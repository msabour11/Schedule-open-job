import frappe
from frappe.utils import now


# create new unique route
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

    emps = frappe.db.get_list(
        "Employee",
        {"status": ["!=", "Active"], "custom_has_open_job": ["!=", True]},
        ignore_permissions=True,
    )
    for emp in emps:
        employee = frappe.get_doc("Employee", emp)
        employees.append(employee)
        # return employee.name

    print("insert new jop openning")

    for i in employees:
        base_route = f"jobs/{i.company.lower()}/{i.designation.lower()}"
        unique_route = generate_unique_route(base_route)
        jop_openning = frappe.get_doc(
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
        jop_openning.insert(ignore_permissions=True)
        # mark custom_has_open_job as true when create open job for this employee
        i.custom_has_open_job = True
        i.save()
    frappe.db.commit()
