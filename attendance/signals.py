from django.db.models.signals import post_save

def send_attendance(sender, instance, created, **kwargs):
    if created:
        client = get_keen_client()
        client.add_event("student_attendance",
                         {"pk":instance.pk, 
                          "student":{}, 
                          "course_section":{}, 
                          "period":instance.period.name, 
                          "date":{}, 
                          "status":{}})
