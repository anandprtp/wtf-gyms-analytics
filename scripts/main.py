import mysql.connector
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import warnings

warnings.filterwarnings('ignore')

# Initialize Faker with Indian locale
fake = Faker(['en_IN'])
# Add more locales if needed
Faker.seed(42)  # For reproducibility
np.random.seed(42)


# Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # change as needed
            password='Manu@7017',  # change as needed
            database='wtf_gyms_latest'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        exit(1)


# Clean all tables before inserting
def clean_tables(connection):
    cursor = connection.cursor()
    tables = ['subscriptions', 'members', 'employees', 'revenue', 'expenses', 'gyms', 'plans', 'leads']  # Added 'leads'

    for table in tables:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"Cleared table: {table}")
        except mysql.connector.Error as err:
            print(f"Error clearing table {table}: {err}")

    connection.commit()
    cursor.close()


# Define gym data
def create_gyms_data():
    gyms_data = [
        {
            'gym_id': 1,
            'gym_name': 'WTF Gym Nayaykhand 3 Indirapuram Ghaziabad',
            'city': 'Ghaziabad',
            'state': 'Uttar Pradesh',
            'open_date': '2023-01-15',
            'status': 'active'
        },
        {
            'gym_id': 2,
            'gym_name': 'WTF Gym Sector 122 Noida',
            'city': 'Noida',
            'state': 'Uttar Pradesh',
            'open_date': '2023-07-10',
            'status': 'active'
        },
        {
            'gym_id': 3,
            'gym_name': 'WTF Gym Gaur Mall RDC Nagar Ghaziabad',
            'city': 'Ghaziabad',
            'state': 'Uttar Pradesh',
            'open_date': '2023-02-05',
            'status': 'active'
        },
        {
            'gym_id': 4,
            'gym_name': 'WTF Exclusive Gym WTT Tower Sector 16 Noida',
            'city': 'Noida',
            'state': 'Uttar Pradesh',
            'open_date': '2023-11-20',
            'status': 'active'
        },
        {
            'gym_id': 5,
            'gym_name': 'WTF Gym Sector 17 Dwarka New Delhi',
            'city': 'New Delhi',
            'state': 'Delhi',
            'open_date': '2023-03-12',
            'status': 'active'
        },
        {
            'gym_id': 6,
            'gym_name': 'WTF Gym Sector 10 Dwarka New Delhi',
            'city': 'New Delhi',
            'state': 'Delhi',
            'open_date': '2023-09-30',
            'status': 'active'
        },
        {
            'gym_id': 7,
            'gym_name': 'WTF Gym Sector 49 Noida',
            'city': 'Noida',
            'state': 'Uttar Pradesh',
            'open_date': '2023-08-15',
            'status': 'active'
        },
        {
            'gym_id': 8,
            'gym_name': 'WTF Gym Sector 70 Noida',
            'city': 'Noida',
            'state': 'Uttar Pradesh',
            'open_date': '2023-01-07',
            'status': 'active'
        },
        {
            'gym_id': 9,
            'gym_name': 'WTF Exclusive Gym Banashankari 3rd Stage Bangalore',
            'city': 'Bangalore',
            'state': 'Karnataka',
            'open_date': '2023-04-22',
            'status': 'active'
        },
        {
            'gym_id': 10,
            'gym_name': 'WTF: Prod Testing Gym Fitness Unit',
            'city': 'Gurgaon',
            'state': 'Haryana',
            'open_date': '2023-11-01',
            'status': 'inactive'  # This one is for testing
        },
        {
            'gym_id': 11,
            'gym_name': 'WTF Gym Parthala Khanjarpur Sector 121 Noida',
            'city': 'Noida',
            'state': 'Uttar Pradesh',
            'open_date': '2023-06-18',
            'status': 'active'
        }
    ]
    return gyms_data


# Define membership plans
def create_plans_data():
    plans_data = [
        {
            'plan_id': 1,
            'plan_name': 'Annual Premium Membership',
            'duration_months': 12,
            'price': 50000.00
        },
        {
            'plan_id': 2,
            'plan_name': 'Half Yearly Premium Membership',
            'duration_months': 6,
            'price': 28000.00
        },
        {
            'plan_id': 3,
            'plan_name': 'Quarterly Premium Membership',
            'duration_months': 3,
            'price': 15000.00
        },
        {
            'plan_id': 4,
            'plan_name': 'Monthly Premium Membership',
            'duration_months': 1,
            'price': 6000.00
        },
        {
            'plan_id': 5,
            'plan_name': 'Day Pass',
            'duration_months': 0,  # Less than a month
            'price': 500.00
        },
        {
            'plan_id': 6,
            'plan_name': 'Annual Standard Membership',
            'duration_months': 12,
            'price': 40000.00
        },
        {
            'plan_id': 7,
            'plan_name': 'Half Yearly Standard Membership',
            'duration_months': 6,
            'price': 22000.00
        },
        {
            'plan_id': 8,
            'plan_name': 'Quarterly Standard Membership',
            'duration_months': 3,
            'price': 12000.00
        },
        {
            'plan_id': 9,
            'plan_name': 'Monthly Standard Membership',
            'duration_months': 1,
            'price': 5000.00
        },
        {
            'plan_id': 10,
            'plan_name': 'Exclusive Annual Membership',
            'duration_months': 12,
            'price': 70000.00
        }
    ]
    return plans_data


# Generate employee data
def generate_employees(gyms_data):
    employees = []
    employee_id = 1

    # Define roles with their distribution
    roles = {
        'Trainer': 0.4,
        'Sales Executive': 0.2,
        'Manager': 0.05,
        'Front Desk': 0.15,
        'Janitor': 0.1,
        'Nutritionist': 0.05,
        'Maintenance': 0.05
    }

    # Ensure each gym has at least one manager, multiple trainers and at least 3 sales execs
    for gym in gyms_data:
        gym_id = gym['gym_id']
        gym_open_date = datetime.strptime(gym['open_date'], '%Y-%m-%d')

        # Add a manager for each gym
        employees.append({
            'employee_id': employee_id,
            'name': fake.name(),
            'role': 'Manager',
            'gym_id': gym_id,
            'date_joined': (gym_open_date + timedelta(days=random.randint(-30, 30))).strftime('%Y-%m-%d')
        })
        employee_id += 1

        # Add 3-5 sales executives for each gym
        for _ in range(random.randint(3, 5)):
            join_date = (gym_open_date + timedelta(days=random.randint(0, 730))).strftime('%Y-%m-%d')
            employees.append({
                'employee_id': employee_id,
                'name': fake.name(),
                'role': 'Sales Executive',
                'gym_id': gym_id,
                'date_joined': join_date
            })
            employee_id += 1

        # Add random number of other staff based on gym size
        num_employees = random.randint(15, 30) if "Exclusive" in gym['gym_name'] else random.randint(10, 20)

        for _ in range(num_employees):
            role = random.choices(list(roles.keys()), list(roles.values()))[0]
            join_date = (gym_open_date + timedelta(days=random.randint(0, 730))).strftime('%Y-%m-%d')

            employees.append({
                'employee_id': employee_id,
                'name': fake.name(),
                'role': role,
                'gym_id': gym_id,
                'date_joined': join_date
            })
            employee_id += 1

    return employees


# Generate member data with realistic Indian names and some duplicates
def generate_members(gyms_data, employees_data, num_members=8000):  # Increased from 5000 to 8000
    members = []
    member_id = 1

    # Duplicate rate: 5% of members will be duplicates
    duplicate_rate = 0.05
    num_unique_members = int(num_members * (1 - duplicate_rate))

    # Create unique members first
    for _ in range(num_unique_members):
        gym_id = random.choice([g['gym_id'] for g in gyms_data if g['status'] == 'active'])
        gym_data = next(g for g in gyms_data if g['gym_id'] == gym_id)
        gym_open_date = datetime.strptime(gym_data['open_date'], '%Y-%m-%d')

        # Get sales executives from this gym
        gym_sales_execs = [e for e in employees_data if e['gym_id'] == gym_id and e['role'] == 'Sales Executive']
        gym_trainers = [e for e in employees_data if e['gym_id'] == gym_id and e['role'] == 'Trainer']

        if not gym_sales_execs or not gym_trainers:
            continue

        join_date = fake.date_between_dates(
            date_start=max(gym_open_date, datetime(2023, 1, 1)),
            date_end=datetime(2025, 3, 31)
        ).strftime('%Y-%m-%d')

        # Generate an Indian name
        gender = random.choice(['male', 'female', 'other'])
        if gender == 'male':
            name = fake.name_male()
        elif gender == 'female':
            name = fake.name_female()
        else:
            name = fake.name()

        # Make some names have different case or extra spaces to simulate data entry issues
        if random.random() < 0.03:
            # Different case
            name = name.upper() if random.random() < 0.5 else name.title()
        if random.random() < 0.02:
            # Extra spaces
            words = name.split()
            name = '  '.join(words) if random.random() < 0.5 else ' '.join(words) + ' '

        age = random.randint(18, 65)

        # Assigned sales exec and trainer
        employee_added_by = random.choice(gym_sales_execs)['employee_id']
        assigned_to_employee = random.choice(gym_trainers)['employee_id'] if random.random() > 0.3 else None

        members.append({
            'member_id': member_id,
            'name': name,
            'gender': gender,
            'age': age,
            'gym_id': gym_id,
            'join_date': join_date,
            'date_added': join_date,
            'employee_added_by': employee_added_by,
            'assigned_to_employee': assigned_to_employee
        })
        member_id += 1

    # Create duplicates
    num_duplicates = num_members - num_unique_members
    original_members = members.copy()

    for _ in range(num_duplicates):
        original = random.choice(original_members)
        duplicate = original.copy()
        duplicate['member_id'] = member_id

        # Slightly alter the duplicate to simulate data entry errors
        if random.random() < 0.7:
            # Change the name slightly
            name = duplicate['name']
            if random.random() < 0.3:
                # Add a typo
                chars = list(name)
                idx = random.randint(0, len(chars) - 1)
                chars[idx] = random.choice('abcdefghijklmnopqrstuvwxyz ')
                duplicate['name'] = ''.join(chars)
            elif random.random() < 0.3:
                # Change case
                duplicate['name'] = name.upper() if random.random() < 0.5 else name.lower()
            else:
                # Add/remove a space
                words = name.split()
                if len(words) > 1:
                    duplicate['name'] = '  '.join(words) if random.random() < 0.5 else ''.join(words)

        # Maybe change the gym
        if random.random() < 0.2:
            new_gym_id = random.choice(
                [g['gym_id'] for g in gyms_data if g['status'] == 'active' and g['gym_id'] != duplicate['gym_id']])
            duplicate['gym_id'] = new_gym_id

            # Update employee references for the new gym
            gym_sales_execs = [e for e in employees_data if
                               e['gym_id'] == new_gym_id and e['role'] == 'Sales Executive']
            gym_trainers = [e for e in employees_data if e['gym_id'] == new_gym_id and e['role'] == 'Trainer']

            if gym_sales_execs:
                duplicate['employee_added_by'] = random.choice(gym_sales_execs)['employee_id']

            if gym_trainers and random.random() > 0.3:
                duplicate['assigned_to_employee'] = random.choice(gym_trainers)['employee_id']
            else:
                duplicate['assigned_to_employee'] = None

        members.append(duplicate)
        member_id += 1

    return members


# Generate subscription data
def generate_subscriptions(members_data, plans_data):
    subscriptions = []
    subscription_id = 1

    for member in members_data:
        member_id = member['member_id']
        join_date = datetime.strptime(member['join_date'], '%Y-%m-%d')

        # Determine how many subscriptions this member has had
        num_subscriptions = np.random.choice([1, 2, 3, 4, 5], p=[0.3, 0.3, 0.2, 0.15, 0.05])

        current_date = join_date
        for i in range(num_subscriptions):
            # Select a plan - weights should match the number of plans (10)
            if i == 0:
                # First subscription weights (10 values matching 10 plans)
                plan_weights = [0.05, 0.1, 0.15, 0.2, 0.02, 0.1, 0.15, 0.1, 0.05, 0.08]
            else:
                # Later subscription weights (10 values)
                plan_weights = [0.2, 0.15, 0.15, 0.1, 0.01, 0.1, 0.1, 0.05, 0.05, 0.09]

            plan_index = np.random.choice(range(len(plans_data)), p=plan_weights)
            plan = plans_data[plan_index]

            start_date = current_date

            if plan['duration_months'] == 0:
                end_date = start_date + timedelta(days=1)
            else:
                # Extend duration for more actives
                duration_months = plan['duration_months'] * random.uniform(1.0, 1.5)
                end_date = start_date + timedelta(days=30 * duration_months)

            today = datetime.now().date()

            # Modified status distribution to favor active subscriptions
            if end_date.date() < today:
                status = 'expired'
            else:
                # Higher chance of active status (70% -> 85%)
                status = np.random.choice(['active', 'expired', 'cancelled'], p=[0.85, 0.1, 0.05])

            # Add anomalies (5% chance)
            if random.random() < 0.05:
                if status == 'active':
                    # Make some very long active subscriptions
                    end_date = start_date + timedelta(days=random.randint(400, 800))
                elif status == 'expired':
                    # Some expired subscriptions that ended very recently
                    if random.random() < 0.4:
                        days_ago = random.randint(1, 15)
                        end_date = datetime.now().date() - timedelta(days=days_ago)
                        end_date = datetime.combine(end_date, datetime.min.time())
                else:
                    # Make some very short subscriptions
                    end_date = start_date + timedelta(days=random.randint(1, 7))

            # Add more anomalies for data variety (2% chance)
            if random.random() < 0.02:
                # Some active subscriptions with unusual extension patterns
                if status == 'active':
                    # Add extreme outliers with very long active durations
                    end_date = start_date + timedelta(days=random.randint(900, 1200))
                # Some subscriptions that were cancelled almost immediately
                elif status == 'cancelled' and random.random() < 0.5:
                    end_date = start_date + timedelta(days=random.randint(1, 3))

            subscriptions.append({
                'subscription_id': subscription_id,
                'member_id': member_id,
                'plan_id': plan['plan_id'],
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'status': status
            })

            subscription_id += 1
            # Shorter gaps between subscriptions
            current_date = end_date + timedelta(days=random.randint(0, 30))

            # Ensure we don't go beyond April 2025
            if current_date > datetime(2025, 4, 30):
                break

    return subscriptions


# Generate revenue data
def generate_revenue(gyms_data, subscriptions_data, plans_data, members_data):
    revenue_data = []
    revenue_id = 1
    subscription_months = set()

    # Get all unique gym IDs
    gym_ids = [g['gym_id'] for g in gyms_data]

    # First pass: Determine all months we need to consider (2023-2025)
    current_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 4, 30)

    while current_date <= end_date:
        subscription_months.add((current_date.year, current_date.month))
        if current_date.month == 12:
            current_date = datetime(current_date.year + 1, 1, 1)
        else:
            current_date = datetime(current_date.year, current_date.month + 1, 1)

    # Sort months chronologically
    subscription_months = sorted(subscription_months)

    # Generate revenue for each gym for each month
    for gym_id in gym_ids:
        gym_data = next(g for g in gyms_data if g['gym_id'] == gym_id)
        open_date = datetime.strptime(gym_data['open_date'], '%Y-%m-%d')

        for year, month in subscription_months:
            month_date = datetime(year, month, 1)

            # Skip if gym wasn't open yet or date is in future
            if month_date < max(open_date, datetime(2023, 1, 1)) or month_date > datetime(2025, 4, 30):
                continue

            # Generate 3-5 revenue records per month per gym
            for record_num in range(random.randint(3, 5)):
                # Calculate subscription revenue for this gym in this month
                month_subscription_revenue = 0

                for sub in subscriptions_data:
                    start_date = datetime.strptime(sub['start_date'], '%Y-%m-%d')
                    end_date = datetime.strptime(sub['end_date'], '%Y-%m-%d')

                    # Check if subscription was active in this month
                    month_start = datetime(year, month, 1)
                    month_end = datetime(year, month + 1, 1) - timedelta(days=1) if month != 12 else datetime(year + 1, 1,
                                                                                                              1) - timedelta(
                        days=1)

                    if start_date <= month_end and end_date >= month_start:
                        member = next((m for m in members_data if m['member_id'] == sub['member_id']), None)

                        if member and member['gym_id'] == gym_id:
                            plan = next((p for p in plans_data if p['plan_id'] == sub['plan_id']), None)

                            if plan:
                                if plan['duration_months'] == 0:  # Day pass
                                    month_subscription_revenue += plan['price'] * random.uniform(0.8, 1.2)
                                else:
                                    # Prorate the monthly value
                                    monthly_value = plan['price'] / plan['duration_months']
                                    days_active = (min(end_date, month_end) - max(start_date, month_start)).days + 1
                                    days_in_month = (month_end - month_start).days + 1
                                    month_subscription_revenue += monthly_value * (days_active / days_in_month) * random.uniform(0.9, 1.1)

                # ===== ENHANCEMENTS START HERE =====
                # Seasonal adjustments
                if month == 1:  # January boost
                    month_subscription_revenue *= random.uniform(1.3, 1.8)
                elif month == 7:  # Summer slump
                    month_subscription_revenue *= random.uniform(0.7, 0.9)

                # Random anomalies (5% chance)
                if random.random() < 0.05:
                    if "Exclusive" in gym_data['gym_name']:
                        month_subscription_revenue *= random.uniform(2.0, 4.0)
                    else:
                        month_subscription_revenue *= random.uniform(1.5, 2.5)

                # Ensure minimum revenue
                month_subscription_revenue = max(month_subscription_revenue, 500000)

                # Other revenue (10-20% of subscription revenue)
                other_revenue = month_subscription_revenue * random.uniform(0.1, 0.2)

                # Special cases for other revenue
                if month == 12:  # Year-end specials
                    other_revenue *= random.uniform(1.5, 2.0)
                elif month == 6:  # Mid-year promotions
                    other_revenue *= random.uniform(1.2, 1.5)
                # ===== ENHANCEMENTS END HERE =====

                total_revenue = month_subscription_revenue + other_revenue

                # Random record date within the month
                record_date = fake.date_between_dates(
                    date_start=datetime(year, month, 1),
                    date_end=datetime(year, month + 1, 1) - timedelta(days=1) if month != 12 else datetime(year + 1, 1, 1) - timedelta(days=1)
                )

                revenue_data.append({
                    'revenue_id': revenue_id,
                    'gym_id': gym_id,
                    'record_date': record_date,
                    'month': year,
                    'month_name': datetime(year, month, 1).strftime('%B'),
                    'subscription_revenue': round(month_subscription_revenue, 2),
                    'other_revenue': round(other_revenue, 2),
                    'total_revenue': round(total_revenue, 2)
                })

                revenue_id += 1

    return revenue_data


def generate_expenses(gyms_data, revenue_data):
    expenses_data = []
    expense_id = 1
    expense_categories = ['rent', 'salaries', 'equipment', 'marketing', 'utilities', 'maintenance', 'supplies',
                          'insurance']

    # Group revenue by gym and month to calculate proper expense ratios
    revenue_by_gym_month = {}
    for revenue in revenue_data:
        key = (revenue['gym_id'], revenue['month'])
        if key not in revenue_by_gym_month:
            revenue_by_gym_month[key] = []
        revenue_by_gym_month[key].append(revenue)

    # Generate expenses based on revenue
    for (gym_id, year), revenues in revenue_by_gym_month.items():
        gym_data = next(g for g in gyms_data if g['gym_id'] == gym_id)
        is_exclusive = "Exclusive" in gym_data['gym_name']
        city = gym_data['city']

        # Get all months for this gym and year
        months = list({datetime.strptime(r['month_name'], '%B').month for r in revenues})

        for month in months:
            # Calculate total revenue for this gym in this month
            month_revenues = [r for r in revenues if datetime.strptime(r['month_name'], '%B').month == month]
            total_monthly_revenue = sum(r['total_revenue'] for r in month_revenues)

            # Lower expense ratio (40-65% of revenue) - REDUCED FROM 60-80%
            expense_ratio = random.uniform(0.4, 0.65)
            total_monthly_expenses = total_monthly_revenue * expense_ratio

            # Generate 5-8 expense records per month
            num_expenses = random.randint(5, 8)
            allocations = np.random.dirichlet(np.ones(num_expenses)) * total_monthly_expenses

            for i in range(num_expenses):
                category = random.choice(expense_categories)
                base_amount = allocations[i]

                # Apply category-specific multipliers
                if category == 'salaries':
                    base_amount *= random.uniform(0.9, 1.1)
                elif category == 'equipment':
                    base_amount *= random.uniform(0.8, 1.3)
                elif category == 'rent':
                    base_amount *= random.uniform(0.95, 1.05)

                # Apply gym type adjustments
                if is_exclusive:
                    base_amount *= random.uniform(1.1, 1.3)
                else:
                    base_amount *= random.uniform(0.9, 1.1)

                # Apply seasonal adjustments
                if month in [12, 1]:  # December/January
                    base_amount *= random.uniform(1.05, 1.15)
                elif month in [6, 7]:  # June/July
                    base_amount *= random.uniform(0.95, 1.05)

                # Random record date within the month
                expense_date = fake.date_between_dates(
                    date_start=datetime(year, month, 1),
                    date_end=datetime(year, month + 1, 1) - timedelta(days=1) if month != 12 else datetime(year + 1, 1,
                                                                                                           1) - timedelta(
                        days=1)
                )

                expenses_data.append({
                    'expense_id': expense_id,
                    'gym_id': gym_id,
                    'record_date': expense_date,
                    'month': year,
                    'month_name': datetime(year, month, 1).strftime('%B'),
                    'category': category,
                    'total_expense': round(base_amount, 2)
                })
                expense_id += 1

    return expenses_data


def generate_leads(gyms_data, employees_data, members_data, subscriptions_data):
    leads_data = []
    lead_id = 1

    # Define lead types and their distribution
    lead_types = {
        'semi_hot': 0.15,
        'hot': 0.1,
        'hot_missed': 0.05,
        'cold': 0.2,
        'warm': 0.15,
        'n/a': 0.35
    }

    # Define lead sources and their distribution
    lead_sources = {
        'renewal': 0.1,
        'referral': 0.15,
        'gym_visit': 0.1,
        'wtf_one_day_plan': 0.05,
        'company_leads': 0.05,
        'unpaid': 0.05,
        'inbound_ads_call': 0.12,
        'trial': 0.08,
        'enquiry': 0.1,
        'btl_marketing': 0.05,
        'mobile_register': 0.05,
        'wati': 0.02,
        'ivr': 0.03,
        'cold_calling': 0.05
    }

    # Define lead statuses
    lead_statuses = ['converted', 'pending']

    # Generate leads for each gym
    for gym in gyms_data:
        gym_id = gym['gym_id']
        gym_open_date = datetime.strptime(gym['open_date'], '%Y-%m-%d')

        # Get sales executives for this gym
        gym_sales_execs = [e for e in employees_data if e['gym_id'] == gym_id and e['role'] == 'Sales Executive']

        if not gym_sales_execs:
            continue

        # Calculate number of leads for this gym (2-3x the number of members)
        gym_members = [m for m in members_data if m['gym_id'] == gym_id]
        num_leads = len(gym_members) * random.uniform(2, 3)

        # Generate the leads
        for _ in range(int(num_leads)):
            # Create date between gym opening and now
            lead_date = fake.date_between_dates(
                date_start=max(gym_open_date, datetime(2023, 1, 1)),
                date_end=datetime(2025, 3, 31)
            )

            # Assign to a sales executive
            assigned_to = random.choice(gym_sales_execs)['employee_id']

            # Determine lead type
            lead_type = random.choices(
                list(lead_types.keys()),
                weights=list(lead_types.values()),
                k=1
            )[0]

            # Determine lead source
            lead_source = random.choices(
                list(lead_sources.keys()),
                weights=list(lead_sources.values()),
                k=1
            )[0]

            # Special case: renewal leads come from existing members
            if lead_source == 'renewal' and gym_members:
                # Try to find a member whose subscription is about to expire
                potential_renewals = []
                for member in gym_members:
                    member_subs = [s for s in subscriptions_data if s['member_id'] == member['member_id']]
                    for sub in member_subs:
                        end_date = datetime.strptime(sub['end_date'], '%Y-%m-%d')
                        lead_datetime = datetime.combine(lead_date, datetime.min.time())
                        if end_date < lead_datetime + timedelta(days=30) and end_date > lead_datetime - timedelta(
                                days=30):
                            potential_renewals.append(member)
                            break

                member_id = random.choice(potential_renewals)['member_id'] if potential_renewals else None
            else:
                member_id = None

            # Determine lead status (converted or pending)
            # Higher quality leads have higher conversion rates
            conversion_rate = {
                'hot': 0.7,
                'semi_hot': 0.5,
                'warm': 0.3,
                'cold': 0.1,
                'hot_missed': 0.2,
                'n/a': 0.05
            }.get(lead_type, 0.2)

            # Source-based adjustments to conversion rate
            source_multiplier = {
                'renewal': 1.5,
                'referral': 1.3,
                'gym_visit': 1.2,
                'cold_calling': 0.6,
                'mobile_register': 0.8
            }.get(lead_source, 1.0)

            conversion_rate = min(0.95, conversion_rate * source_multiplier)

            status = 'converted' if random.random() < conversion_rate else 'pending'

            # For converted leads, set conversion date and potential value
            if status == 'converted':
                # Conversion takes between 1-30 days
                conversion_days = int(random.expovariate(1 / 7)) + 1  # Average 7 days
                conversion_date = lead_date + timedelta(days=min(conversion_days, 30))

                # Make sure conversion date isn't in the future
                if conversion_date and datetime.combine(conversion_date, datetime.min.time()) > datetime(2025, 3, 31):
                    conversion_date = datetime(2025, 3, 31).date()

                # Determine potential value based on lead type
                base_value = random.uniform(8000, 50000)
                value_multiplier = {
                    'hot': 1.5,
                    'semi_hot': 1.2,
                    'warm': 1.0,
                    'cold': 0.7,
                    'hot_missed': 0.9,
                    'n/a': 0.5
                }.get(lead_type, 1.0)

                potential_value = base_value * value_multiplier

                # Seasonal adjustments to value
                month = conversion_date.month
                if month == 1:  # January (new year resolutions)
                    potential_value *= random.uniform(1.2, 1.5)
                elif month in [6, 7]:  # Summer months
                    potential_value *= random.uniform(0.8, 0.9)
            else:
                conversion_date = None
                potential_value = random.uniform(5000, 40000)  # Estimated value for pending leads

            # Calculate response time (in hours)
            response_time = None
            if lead_type in ['hot', 'semi_hot']:
                response_time = random.uniform(0.5, 8)  # 30 min to 8 hours
            elif lead_type in ['warm', 'hot_missed']:
                response_time = random.uniform(4, 24)  # 4 to 24 hours
            else:
                response_time = random.uniform(12, 72)  # 12 to 72 hours

            # Add some outliers
            if random.random() < 0.05:
                response_time = random.uniform(72, 168)  # 3-7 days (very slow)

            lead = {
                'lead_id': lead_id,
                'gym_id': gym_id,
                'lead_date': lead_date.strftime('%Y-%m-%d'),
                'lead_type': lead_type,
                'lead_source': lead_source,
                'status': status,
                'assigned_to': assigned_to,
                'member_id': member_id,
                'response_time_hours': round(response_time, 1) if response_time else None,
                'conversion_date': conversion_date.strftime('%Y-%m-%d') if conversion_date else None,
                'potential_value': round(potential_value, 2) if potential_value else None
            }

            leads_data.append(lead)
            lead_id += 1

    return leads_data


# Insert data into tables
def insert_gyms(connection, gyms_data):
    cursor = connection.cursor()
    for gym in gyms_data:
        query = """
        INSERT INTO gyms (gym_id, gym_name, city, state, open_date, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            gym['gym_id'],
            gym['gym_name'],
            gym['city'],
            gym['state'],
            gym['open_date'],
            gym['status']
        )
        cursor.execute(query, values)

    connection.commit()
    cursor.close()
    print(f"Inserted {len(gyms_data)} gyms")


def insert_plans(connection, plans_data):
    cursor = connection.cursor()
    for plan in plans_data:
        query = """
        INSERT INTO plans (plan_id, plan_name, duration_months, price)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            plan['plan_id'],
            plan['plan_name'],
            plan['duration_months'],
            plan['price']
        )
        cursor.execute(query, values)

    connection.commit()
    cursor.close()
    print(f"Inserted {len(plans_data)} plans")


def insert_employees(connection, employees_data):
    cursor = connection.cursor()
    for employee in employees_data:
        query = """
        INSERT INTO employees (employee_id, name, role, gym_id, date_joined)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            employee['employee_id'],
            employee['name'],
            employee['role'],
            employee['gym_id'],
            employee['date_joined']
        )
        cursor.execute(query, values)

    connection.commit()
    cursor.close()
    print(f"Inserted {len(employees_data)} employees")


def insert_members(connection, members_data):
    cursor = connection.cursor()
    for member in members_data:
        query = """
        INSERT INTO members (member_id, name, gender, age, gym_id, join_date, date_added, employee_added_by, assigned_to_employee)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            member['member_id'],
            member['name'],
            member['gender'],
            member['age'],
            member['gym_id'],
            member['join_date'],
            member['date_added'],
            member['employee_added_by'],
            member['assigned_to_employee']
        )
        cursor.execute(query, values)

    connection.commit()
    cursor.close()
    print(f"Inserted {len(members_data)} members")


def insert_subscriptions(connection, subscriptions_data):
    cursor = connection.cursor()
    for subscription in subscriptions_data:
        query = """
        INSERT INTO subscriptions (subscription_id, member_id, plan_id, start_date, end_date, status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            subscription['subscription_id'],
            subscription['member_id'],
            subscription['plan_id'],
            subscription['start_date'],
            subscription['end_date'],
            subscription['status']
        )
        cursor.execute(query, values)

    connection.commit()
    cursor.close()
    print(f"Inserted {len(subscriptions_data)} subscriptions")


def insert_revenue(connection, revenue_data):
    cursor = connection.cursor()
    for revenue in revenue_data:
        query = """
        INSERT INTO revenue (revenue_id, gym_id, record_date, month, month_name, subscription_revenue, other_revenue)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            revenue['revenue_id'],
            revenue['gym_id'],
            revenue['record_date'],
            revenue['month'],
            revenue['month_name'],
            revenue['subscription_revenue'],
            revenue['other_revenue']
        )
        cursor.execute(query, values)

    connection.commit()
    cursor.close()
    print(f"Inserted {len(revenue_data)} revenue records")


def insert_expenses(connection, expenses_data):
    cursor = connection.cursor()
    for expense in expenses_data:
        query = """
        INSERT INTO expenses (expense_id, gym_id, record_date, month, month_name, category, total_expense)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            expense['expense_id'],
            expense['gym_id'],
            expense['record_date'],
            expense['month'],
            expense['month_name'],
            expense['category'],
            expense['total_expense']
        )
        cursor.execute(query, values)

    connection.commit()
    cursor.close()
    print(f"Inserted {len(expenses_data)} expense records")

def insert_leads(connection, leads_data):
    cursor = connection.cursor()
    for lead in leads_data:
        query = """
        INSERT INTO leads (lead_id, gym_id, lead_date, lead_type, lead_source, status, 
                          assigned_to, member_id, response_time_hours, conversion_date, potential_value)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            lead['lead_id'],
            lead['gym_id'],
            lead['lead_date'],
            lead['lead_type'],
            lead['lead_source'],
            lead['status'],
            lead['assigned_to'],
            lead['member_id'],
            lead['response_time_hours'],
            lead['conversion_date'],
            lead['potential_value']
        )
        cursor.execute(query, values)

    connection.commit()
    cursor.close()
    print(f"Inserted {len(leads_data)} leads")


def main():
    # Connect to database
    connection = get_db_connection()

    # Clean all tables
    clean_tables(connection)

    # Generate data
    gyms_data = create_gyms_data()
    plans_data = create_plans_data()

    # Insert base data
    insert_gyms(connection, gyms_data)
    insert_plans(connection, plans_data)

    # Generate and insert employee data
    employees_data = generate_employees(gyms_data)
    insert_employees(connection, employees_data)

    # Generate and insert member data - INCREASED TO 8000
    members_data = generate_members(gyms_data, employees_data, num_members=8000)
    insert_members(connection, members_data)

    # Generate and insert subscription data
    subscriptions_data = generate_subscriptions(members_data, plans_data)
    insert_subscriptions(connection, subscriptions_data)

    # Generate and insert revenue data
    revenue_data = generate_revenue(gyms_data, subscriptions_data, plans_data, members_data)
    insert_revenue(connection, revenue_data)

    # Generate and insert expense data
    expenses_data = generate_expenses(gyms_data, revenue_data)
    insert_expenses(connection, expenses_data)

    # Generate and insert lead data
    leads_data = generate_leads(gyms_data, employees_data, members_data, subscriptions_data)
    insert_leads(connection, leads_data)

    print("Database population completed successfully!")
    connection.close()


if __name__ == "__main__":
    main()