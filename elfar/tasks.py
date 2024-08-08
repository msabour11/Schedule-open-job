# import frappe
# from frappe.utils import now, today


# # create new unique route
# def generate_unique_route(base_route):
#     exists = frappe.db.exists("Job Opening", {"route": base_route})
#     counter = 1
#     new_route = base_route  # Initialize new_route with base_route
#     while exists:
#         new_route = f"{base_route}-{counter}"
#         exists = frappe.db.exists("Job Opening", {"route": new_route})
#         counter += 1
#     return new_route


# @frappe.whitelist(allow_guest=True)
# def create_job_openning():
#     employees = []
#     tody = today()

#     emps = frappe.db.get_list(
#         "Employee",
#         {
#             "custom_has_open_job": ["!=", True],
#             "resignation_letter_date": ["=", tody],
#         },
#         ignore_permissions=True,
#     )
#     for emp in emps:
#         employee = frappe.get_doc("Employee", emp)
#         employees.append(employee)
#         # return employee.name

#     print("insert new jop openning")

#     for i in employees:
#         base_route = f"jobs/{i.company.lower()}/{i.designation.lower()}"
#         unique_route = generate_unique_route(base_route)
#         jop_openning = frappe.get_doc(
#             {
#                 "doctype": "Job Opening",
#                 "job_title": i.designation,
#                 "designation": i.designation,
#                 "status": "Open",
#                 "company": i.company,
#                 "department": i.department,
#                 "employment_type": i.employment_type,
#                 "posted_on": now(),
#                 "route": unique_route,
#             }
#         )
#         jop_openning.insert(ignore_permissions=True)
#         # mark custom_has_open_job as true when create open job for this employee
#         i.custom_has_open_job = True
#         i.save()
#     frappe.db.commit()

import frappe
from frappe.utils import now, today

# Create a new unique route
def generate_unique_route(base_route):
    exists = frappe.db.exists("Job Opening", {"route": base_route})
    counter = 1
    new_route = base_route  # Initialize new_route with base_route
    while exists:
        new_route = f"{base_route}-{counter}"
        exists = frappe.db.exists("Job Opening", {"route": new_route})
        counter += 1
    return new_route

@frappe.whitelist(allow_guest=True)
def create_job_openning():
    employees = []
    current_date = today()  # Corrected variable name

    # Fetch only required fields
    emps = frappe.db.get_list(
        "Employee",
        filters={
            "custom_has_open_job": ["!=", True],
            "resignation_letter_date": ["=", current_date],
        },
        fields=["name", "company", "designation", "department", "employment_type"],
        ignore_permissions=True,
    )
    
    for emp in emps:
        employees.append(frappe.get_doc("Employee", emp.name))

    print("Inserting new job opening")

    for i in employees:
        if i.company and i.designation:
            base_route = f"jobs/{i.company.lower()}/{i.designation.lower()}"
            unique_route = generate_unique_route(base_route)
            job_opening = frappe.get_doc(
                {
                    "doctype": "Job Opening",
                    "job_title": i.designation,
                    "designation": i.designation,
                    "status": "Open",
                    "company": i.company,
                    "department": i.department,
                    "employment_type": i.employment_type,
                    "posted_on": now(),
                    "route": unique_route,
                }
            )
            job_opening.insert(ignore_permissions=True)

            # Mark custom_has_open_job as True when a job opening is created for this employee
            i.custom_has_open_job = True
            i.save()

    frappe.db.commit()



@frappe.whitelist(allow_guest=True)
def mark_employee_inactive():
    employees = []
    tody = today()

    emps = frappe.db.get_list(
        "Employee",
        {
            "relieving_date": ["=", tody],
            "custom_is_exit":["=",False]
        },
        ignore_permissions=True,
    )
    for emp in emps:
        employee = frappe.get_doc("Employee", emp)
        employees.append(employee)
    for emp in employees:
        emp.custom_is_exit = True
        emp.status = "Inactive"
        emp.flags.ignore_permissions = True
        emp.save()
    frappe.db.commit()

    # return emps
