import random
import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.home.models import (
    Truck, Driver, Customer,
    TruckExpense, FuelEntry, TruckMaintenanceRecord,
    TruckLoad, HosLog, TruckInvoice, TruckLineItem, TollEntry
)

class Command(BaseCommand):
    help = 'Seed the database with trucking test data'

    def handle(self, *args, **options):
        # 1) Create Trucks
        trucks = []
        for i in range(1, 11):
            t, _ = Truck.objects.get_or_create(
                name=f"Truck {i}",
                defaults={
                    "license_plate": f"PLT{i:04d}",
                    "odometer": random.randint(50_000, 300_000),
                    "active": True
                }
            )
            trucks.append(t)
        self.stdout.write(f"Created {len(trucks)} trucks")

        # 2) Create Users & Drivers
        drivers = []
        for i in range(1, 21):
            u, _ = User.objects.get_or_create(
                username=f"driver{i}",
                defaults={"email": f"driver{i}@fleet.com", "password": "pbkdf2_sha256$..."}
            )
            d, _ = Driver.objects.get_or_create(
                user=u,
                defaults={
                    "cdl_number": f"CDL{random.randint(10000,99999)}",
                    "phone": f"555-{random.randint(100,999)}-{random.randint(1000,9999)}",
                    "hire_date": datetime.date.today() - datetime.timedelta(days=random.randint(0,1000))
                }
            )
            drivers.append(d)
        self.stdout.write(f"Created {len(drivers)} drivers")

        # 3) Create Customers
        customer_names = ["Acme Freight","Atlas Logistics","RoadRunner LLC",
                          "BlueLine Transport","NorthStar Haulers","EastCoast Carriers"]
        customers = []
        for name in customer_names:
            c, _ = Customer.objects.get_or_create(
                name=name,
                defaults={
                    "contact_name": f"{name.split()[0]} Manager",
                    "contact_email": f"contact@{name.lower().replace(' ','')}.com",
                    "contact_phone": f"555-{random.randint(200,799)}-{random.randint(1000,9999)}",
                }
            )
            customers.append(c)
        self.stdout.write(f"Created {len(customers)} customers")

        # 4) Create Loads
        loads = []
        for _ in range(200):
            truck = random.choice(trucks)
            driver = random.choice(drivers)
            customer = random.choice(customers)
            start = datetime.date.today() - datetime.timedelta(days=random.randint(0,60))
            done = random.choice([True, False])
            completed = (start + datetime.timedelta(days=random.randint(0,5))) if done else None
            pay = Decimal(random.uniform(800,5000)).quantize(Decimal("0.01"))
            miles = random.randint(100,1200)
            hrs_tot = Decimal(random.uniform(2,20)).quantize(Decimal("0.1"))
            hrs_lu  = Decimal(random.uniform(0.5,3)).quantize(Decimal("0.1"))
            l, _ = TruckLoad.objects.get_or_create(
                truck=truck, driver=driver, customer=customer, date_started=start,
                defaults={
                    "date_completed": completed,
                    "time_loaded": datetime.time(hour=random.randint(0,23), minute=random.choice([0,15,30,45])),
                    "time_unloaded": (datetime.time(hour=random.randint(0,23), minute=random.choice([0,15,30,45])) if done else None),
                    "pay_amount": pay,
                    "miles": miles,
                    "hours_total": hrs_tot,
                    "hours_load_unload": hrs_lu,
                    "pickup_address": "123 Origin St",
                    "dropoff_address": "456 Destination Ave",
                    "route_distance": miles,
                    "status": "completed" if done else "active"
                }
            )
            loads.append(l)
        self.stdout.write(f"Created {len(loads)} loads")

        # 5) Expenses
        exp_count = 0
        for _ in range(300):
            tr = random.choice(trucks)
            d = datetime.date.today() - datetime.timedelta(days=random.randint(0,90))
            amt = Decimal(random.uniform(50,1000)).quantize(Decimal("0.01"))
            e, created = TruckExpense.objects.get_or_create(
                truck=tr, date_incurred=d,
                description=random.choice(["Oil Change","Brake Repair","Tire Replacement","Engine Tune"]),
                defaults={"amount": amt, "category": random.choice(["maintenance","repair","parts"]) }
            )
            if created:
                exp_count += 1
        self.stdout.write(f"Created {exp_count} expenses")

        # 6) Fuel Entries
        fuel_count = 0
        for _ in range(300):
            tr = random.choice(trucks)
            d = datetime.date.today() - datetime.timedelta(days=random.randint(0,90))
            gals = Decimal(random.uniform(20,100)).quantize(Decimal("0.1"))
            ppg  = Decimal(random.uniform(2.5,4.0)).quantize(Decimal("0.01"))
            f, created = FuelEntry.objects.get_or_create(
                truck=tr, date=d,
                defaults={"gallons": gals, "price_per_gallon": ppg, "odometer_reading": tr.odometer + random.randint(100,500)}
            )
            if created:
                fuel_count += 1
        self.stdout.write(f"Created {fuel_count} fuel entries")

        # 7) Maintenance Records
        mr_count = 0
        for _ in range(150):
            tr = random.choice(trucks)
            d = datetime.date.today() - datetime.timedelta(days=random.randint(0,180))
            cost = Decimal(random.uniform(100,2000)).quantize(Decimal("0.01"))
            mr, created = TruckMaintenanceRecord.objects.get_or_create(
                truck=tr, date=d,
                defaults={"odometer": random.randint(50000,300000),
                          "description": random.choice(["Full Service","Transmission Check","Alignment"]),
                          "cost": cost}
            )
            if created:
                mr_count += 1
        self.stdout.write(f"Created {mr_count} maintenance records")

        # 8) HOS Logs
        hos_count = 0
        for _ in range(150):
            d = datetime.date.today() - datetime.timedelta(days=random.randint(0,30))
            dr = random.choice(drivers)
            on = datetime.time(8,0)
            off = datetime.time(hour=8+random.randint(4,12), minute=0)
            dur = (datetime.datetime.combine(d, off) - datetime.datetime.combine(d, on)).seconds / 3600
            hrs = Decimal(dur).quantize(Decimal("0.1"))
            h, created = HosLog.objects.get_or_create(
                driver=dr, date=d,
                defaults={"on_duty_time": on, "off_duty_time": off, "driving_hours": hrs}
            )
            if created:
                hos_count += 1
        self.stdout.write(f"Created {hos_count} HOS logs")

        # 9) Invoices & LineItems
        inv_count = 0
        for load in random.sample(loads, k=min(80, len(loads))):
            issue_date = (load.date_completed or load.date_started) + datetime.timedelta(days=1)
            inv, created = TruckInvoice.objects.get_or_create(
                load=load, invoice_number=f"INV-{load.pk:04d}",
                defaults={"date_issued": issue_date, "total_amount": load.pay_amount,
                          "paid": random.choice([True,False]),
                          "paid_date": (issue_date + datetime.timedelta(days=random.randint(1,30))) if random.choice([True,False]) else None}
            )
            if created:
                inv_count += 1
                TruckLineItem.objects.create(
                    invoice=inv, description="Freight Charge",
                    quantity=Decimal("1.00"), unit_price=load.pay_amount, total_price=load.pay_amount
                )
        self.stdout.write(f"Created {inv_count} invoices + line items")

        # 10) Toll Entries
        toll_count = 0
        for load in random.sample(loads, k=min(80, len(loads))):
            d = load.date_started + datetime.timedelta(days=random.randint(0,2))
            amt = Decimal(random.uniform(5,50)).quantize(Decimal("0.01"))
            t, created = TollEntry.objects.get_or_create(
                load=load, date=d,
                defaults={"toll_location": random.choice(["Bridge","Tunnel","Highway"]), "amount": amt}
            )
            if created:
                toll_count += 1
        self.stdout.write(f"Created {toll_count} toll entries")

        self.stdout.write(self.style.SUCCESS("✅ All test data seeded!"))
