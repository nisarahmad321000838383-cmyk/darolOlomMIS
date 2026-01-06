# Generated migration to convert class_name CharField to school_class ForeignKey

from django.db import migrations, models
import django.db.models.deletion


def migrate_class_names_forward(apps, schema_editor):
    """
    Forward migration: Convert existing class_name text values to SchoolClass ForeignKey references.
    Creates SchoolClass objects for any class names that don't exist yet.
    """
    Student = apps.get_model('core', 'Student')
    SchoolClass = apps.get_model('core', 'SchoolClass')
    
    # Get all unique class names from students
    students = Student.objects.exclude(class_name='').exclude(class_name__isnull=True)
    
    for student in students:
        if student.class_name:
            # Get or create the SchoolClass object
            school_class, created = SchoolClass.objects.get_or_create(
                name=student.class_name
            )
            # Assign the ForeignKey
            student.school_class = school_class
            student.save(update_fields=['school_class'])


def migrate_class_names_backward(apps, schema_editor):
    """
    Reverse migration: Convert SchoolClass ForeignKey back to class_name text.
    """
    Student = apps.get_model('core', 'Student')
    
    for student in Student.objects.filter(school_class__isnull=False):
        student.class_name = student.school_class.name
        student.save(update_fields=['class_name'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_schoolclass_semester'),
    ]

    operations = [
        # Step 1: Add the new school_class ForeignKey field (nullable for now)
        migrations.AddField(
            model_name='student',
            name='school_class',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='students',
                to='core.schoolclass',
                verbose_name='صنف'
            ),
        ),
        
        # Step 2: Migrate existing data from class_name to school_class
        migrations.RunPython(
            migrate_class_names_forward,
            reverse_code=migrate_class_names_backward
        ),
        
        # Step 3: Remove the old class_name CharField
        migrations.RemoveField(
            model_name='student',
            name='class_name',
        ),
    ]
