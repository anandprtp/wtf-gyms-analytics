# WTF Gyms Analytics - Technical Documentation

## Data Generation Process

### Overview
This project utilizes Python to generate synthetic business data that realistically simulates WTF Gyms' operations. The synthetic data creation process was designed to provide comprehensive datasets for business intelligence development without exposing actual customer information.

### Python Libraries Used
- **NumPy**: For numerical operations and random data generation
- **Faker**: To create realistic names, addresses, and other personal information
- **Pandas**: For data manipulation and preparation
- **MySQL Connector**: For database integration

### Data Structure
The generated data follows a relational database structure with the following key tables:

1. **Gyms**
   - GymID (PK)
   - GymName
   - City
   - State
   - OpeningDate
   - TargetRevenue
   - TargetMembers

2. **Members**
   - MemberID (PK)
   - FirstName
   - LastName
   - Email
   - Phone
   - JoinDate
   - GymID (FK)
   - SubscriptionType

3. **Subscriptions**
   - SubscriptionID (PK)
   - MemberID (FK)
   - StartDate
   - EndDate
   - Status (Active/Canceled/Expired)
   - MonthlyFee

4. **Leads**
   - LeadID (PK)
   - FirstName
   - LastName
   - Email
   - Phone
   - LeadSource
   - LeadDate
   - Status (Hot/Warm/Cold)
   - ConversionDate
   - GymID (FK)
   - AssignedEmployeeID (FK)

5. **Employees**
   - EmployeeID (PK)
   - FirstName
   - LastName
   - Position
   - HireDate
   - GymID (FK)

6. **Transactions**
   - TransactionID (PK)
   - MemberID (FK)
   - TransactionDate
   - Amount
   - PaymentMethod
   - TransactionType

### Data Generation Logic

#### Realistic Member Distribution
- Member join dates follow a growth trend mirroring WTF Gyms' expansion timeline
- Member distribution across gyms is weighted by location population density
- Subscription types follow realistic distribution based on market research

#### Lead Conversion Simulation
- Lead sources include digital marketing, referrals, walk-ins, and partner programs
- Conversion rates vary by lead source and assigned employee
- Conversion time follows a probability distribution with most conversions occurring within 1-14 days

#### Revenue Calculation
- Base subscription rate of ₹599/month
- Premium subscription options with additional services
- One-time registration fees
- Special promotions and discounts applied realistically

## Power BI Development

### Data Modeling
The Power BI solution implements a star schema with the following structure:
- **Fact Tables**: Subscriptions, Transactions, Lead Conversions
- **Dimension Tables**: Date, Gym, Member, Employee, Subscription Type, Lead Source

### DAX Measures
Over 54 custom DAX measures were developed, including:

#### Revenue Metrics
```
Total Revenue = 
SUM(Transactions[Amount])

Monthly Revenue = 
CALCULATE(
    [Total Revenue],
    DATESINPERIOD(
        'Date'[Date],
        LASTDATE('Date'[Date]),
        -1,
        MONTH
    )
)

Revenue Growth % = 
DIVIDE(
    [Monthly Revenue] - [Previous Month Revenue],
    [Previous Month Revenue],
    0
)
```

#### Membership Metrics
```
Total Members = 
DISTINCTCOUNT(Members[MemberID])

Active Subscriptions = 
CALCULATE(
    COUNTROWS(Subscriptions),
    Subscriptions[Status] = "Active"
)

Gym Retention Rate = 
DIVIDE(
    CALCULATE(
        DISTINCTCOUNT(Members[MemberID]),
        FILTER(
            Members,
            DATEDIFF(Members[JoinDate], TODAY(), MONTH) > 3
        )
    ),
    [Total Members],
    0
)
```

#### Lead Conversion Metrics
```
Overall Conversion Rate = 
DIVIDE(
    CALCULATE(
        COUNTROWS(Leads),
        NOT(ISBLANK(Leads[ConversionDate]))
    ),
    COUNTROWS(Leads),
    0
)

Avg Conversion Time = 
AVERAGEX(
    FILTER(
        Leads,
        NOT(ISBLANK(Leads[ConversionDate]))
    ),
    DATEDIFF(Leads[LeadDate], Leads[ConversionDate], DAY)
)
```

### Power Query Transformations

#### Date Table Creation
```
let
    Source = List.Dates(#date(2023, 1, 1), 730, #duration(1, 0, 0, 0)),
    #"Converted to Table" = Table.FromList(Source, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
    #"Renamed Columns" = Table.RenameColumns(#"Converted to Table",{{"Column1", "Date"}}),
    #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Year", each Date.Year([Date])),
    #"Added Custom1" = Table.AddColumn(#"Added Custom", "Month Number", each Date.Month([Date])),
    #"Added Custom2" = Table.AddColumn(#"Added Custom1", "Month Name", each Date.MonthName([Date])),
    #"Added Custom3" = Table.AddColumn(#"Added Custom2", "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date]))),
    #"Added Custom4" = Table.AddColumn(#"Added Custom3", "Month-Year", each [Month Name] & "-" & Text.From([Year])),
    #"Added Custom5" = Table.AddColumn(#"Added Custom4", "Week of Year", each Date.WeekOfYear([Date])),
    #"Added Custom6" = Table.AddColumn(#"Added Custom5", "Weekday Name", each Date.DayOfWeekName([Date])),
    #"Added Custom7" = Table.AddColumn(#"Added Custom6", "Start of Month", each Date.StartOfMonth([Date]))
in
    #"Added Custom7"
```

#### City Initials Extraction
```
let
    Source = Table.AddColumn(
        Gyms, 
        "City Initials", 
        each Text.Combine(
            List.Transform(
                Text.Split([City], " "), 
                each Text.Start(_, 1)
            )
        )
    )
in
    Source
```

### UI/UX Design Elements

The dashboard follows WTF Gyms' brand guidelines with:
- Primary color: #FF0954 (Hot Pink)
- Secondary color: #121212 (Black)
- Accent color: #FFFFFF (White)

Custom backgrounds were created in Figma with the following design principles:
- Dark mode to enhance data visualization contrast
- Subtle gradient effects for depth
- Consistent placement of navigation elements
- Integrated brand elements and logo

## Optimization Techniques

### Performance Optimization
- Disabled unnecessary data loads
- Implemented query folding where possible
- Used categorical data types for text columns
- Created calculated tables only when necessary
- Implemented incremental refresh policy

### Visual Optimization
- Limited visuals per page to maintain performance
- Used consistent color scheme across all visuals
- Implemented drillthrough filters instead of complex filter relationships
- Optimized tooltip pages for minimal load time

## Deployment Strategy

The Power BI report is published to the Power BI Service with:
- Scheduled refresh setup for daily updates
- Row-level security (RLS) implementation for gym-specific views
- Report subscription configured for key stakeholders
- Usage metrics tracking to monitor dashboard engagement