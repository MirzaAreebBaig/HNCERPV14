import frappe
import datetime

#-------------------
def send_notification_about_item_expiry():
    items = frappe.db.sql("""
                select 
                    name, item_name, end_of_life
                from
                    tabItem
                where
                    disabled = 0
            """, as_dict=1)

    if items:
        for item in items:
            today = datetime.date.today()
            if today < item.end_of_life:
                end_of_life = item.end_of_life
                diff = end_of_life - today
                if diff.days <= 15:
                    notification = frappe.get_doc('Notification', 'Item Getting Expired')
                    doc = frappe.get_doc('Item', item.name)
                    doc.days = diff.days
                    args={'doc': doc}

                    recipients, cc, bb = notification.get_list_of_recipients(doc, args)

                    frappe.enqueue(method=frappe.sendmail, recipients=recipients, sender=None, now=True,
                        subject=frappe.render_template(notification.subject, args), message=frappe.render_template(notification.message, args))


