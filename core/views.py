from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.http import FileResponse, Http404
from django.conf import settings
import os

from .models import Student, SchoolClass, Subject, Teacher
from .forms import StudentForm, SchoolClassForm, SubjectForm, TeacherForm
import json
from django.utils.safestring import mark_safe


def student_create(request):
	"""فرم ثبت دانش‌آموز جدید (فارسی)."""
	if request.method == 'POST':
		form = StudentForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'دانش‌آموز با موفقیت ثبت شد.')
			return redirect(reverse('core:student_list'))
	else:
		form = StudentForm()
	# Pass available class names so the template can provide a searchable selector
	class_names = list(SchoolClass.objects.values_list('name', flat=True))
	return render(request, 'core/student_form_clean.html', {'form': form, 'class_names': class_names})


def student_list(request):
	"""نمایش لیست دانش‌آموزان با قابلیت جستجو و صفحه‌بندی (20 در هر صفحه)."""
	q = request.GET.get('q', '').strip()
	students = Student.objects.all().order_by('-created_at')
	if q:
		students = students.filter(
			Q(name__icontains=q) | Q(father_name__icontains=q) | Q(mobile_number__icontains=q)
		)

	paginator = Paginator(students, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'q': q,
		'page_obj': page_obj,
	}
	return render(request, 'core/student_list.html', context)


def teacher_list(request):
	"""نمایش لیست اساتید مشابه لیست دانش‌آموزان با جستجو و صفحه‌بندی."""
	q = request.GET.get('q', '').strip()
	teachers = Teacher.objects.all().order_by('-created_at')
	if q:
		teachers = teachers.filter(
			Q(name__icontains=q) | Q(father_name__icontains=q) | Q(id_number__icontains=q)
		)

	paginator = Paginator(teachers, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'q': q,
		'page_obj': page_obj,
	}
	return render(request, 'core/teacher_list.html', context)


def teacher_create(request):
	"""Create a new Teacher. Classes and subjects are provided as searchable tags from frontend."""
	if request.method == 'POST':
		form = TeacherForm(request.POST, request.FILES)
		if form.is_valid():
			teacher = form.save()
			# process classes and subjects provided as repeated fields
			class_names = request.POST.getlist('classes')
			subject_names = request.POST.getlist('subjects')
			semester_values = request.POST.getlist('semesters')
			if class_names:
				classes_qs = SchoolClass.objects.filter(name__in=class_names)
				teacher.classes.set(classes_qs)
			if subject_names:
				sub_qs = Subject.objects.filter(name__in=subject_names)
				teacher.subjects.set(sub_qs)
			# handle semesters: create/get Semester objects for given numbers
			if semester_values:
				from .models import Semester
				sem_qs = []
				def persian_to_ascii(s: str) -> str:
					# convert Persian digits to ascii digits if present
					mapping = {
						'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
						'۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
					}
					return ''.join(mapping.get(ch, ch) for ch in s)

				for s in semester_values:
					s_norm = persian_to_ascii(s.strip())
					try:
						num = int(s_norm)
					except ValueError:
						continue
					sem, _ = Semester.objects.get_or_create(number=num)
					sem_qs.append(sem)
				teacher.semesters.set(sem_qs)
			messages.success(request, 'استاد با موفقیت ثبت شد.')
			return redirect(reverse('core:teacher_list'))
	else:
		form = TeacherForm()

	class_names = list(SchoolClass.objects.values_list('name', flat=True))
	subject_names = list(Subject.objects.values_list('name', flat=True))
	# semester options as objects with value (ascii) and label (persian)
	pers_map = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴'}
	semester_names = [{'value': str(n), 'label': ''.join(pers_map.get(ch, ch) for ch in str(n))} for n in range(1, 5)]
	return render(request, 'core/teacher_form.html', {'form': form, 'class_names': class_names, 'subject_names': subject_names, 'semester_names': semester_names})


def teacher_edit(request, pk):
	teacher = get_object_or_404(Teacher, pk=pk)
	if request.method == 'POST':
		form = TeacherForm(request.POST, request.FILES, instance=teacher)
		if form.is_valid():
			teacher = form.save()
			class_names = request.POST.getlist('classes')
			subject_names = request.POST.getlist('subjects')
			semester_values = request.POST.getlist('semesters')
			if class_names is not None:
				classes_qs = SchoolClass.objects.filter(name__in=class_names)
				teacher.classes.set(classes_qs)
			if subject_names is not None:
				sub_qs = Subject.objects.filter(name__in=subject_names)
				teacher.subjects.set(sub_qs)
			if semester_values is not None:
				from .models import Semester
				sem_qs = []
				def persian_to_ascii(s: str) -> str:
					mapping = {'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'}
					return ''.join(mapping.get(ch, ch) for ch in s)

				for s in semester_values:
					s_norm = persian_to_ascii(s.strip())
					try:
						num = int(s_norm)
					except ValueError:
						continue
					sem, _ = Semester.objects.get_or_create(number=num)
					sem_qs.append(sem)
				teacher.semesters.set(sem_qs)
			messages.success(request, 'اطلاعات استاد با موفقیت بروزرسانی شد.')
			return redirect(reverse('core:teacher_list'))
	else:
		form = TeacherForm(instance=teacher)

	class_names = list(SchoolClass.objects.values_list('name', flat=True))
	subject_names = list(Subject.objects.values_list('name', flat=True))
	# current selections to prefill tags
	teacher_classes = list(teacher.classes.values_list('name', flat=True))
	teacher_subjects = list(teacher.subjects.values_list('name', flat=True))
	teacher_semesters = list(teacher.semesters.values_list('number', flat=True))
	pers_map = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴'}
	semester_names = [{'value': str(n), 'label': ''.join(pers_map.get(ch, ch) for ch in str(n))} for n in range(1, 5)]
	return render(request, 'core/teacher_form.html', {
		'form': form,
		'class_names': class_names,
		'subject_names': subject_names,
		'teacher_classes': teacher_classes,
		'teacher_subjects': teacher_subjects,
		'teacher_semesters': [str(s) for s in teacher_semesters],
		'semester_names': semester_names,
	})


def teacher_delete(request, pk):
	teacher = get_object_or_404(Teacher, pk=pk)
	if request.method == 'POST':
		teacher.delete()
		messages.success(request, 'استاد حذف شد.')
		return redirect(reverse('core:teacher_list'))
	return render(request, 'core/class_confirm_delete.html', {'klass': teacher})


def logo(request):
	"""Serve the app logo stored at core/images/logo.jpg during development.

	This keeps the template simple and doesn't require moving files into
	the static directory. In production, serve static assets via a proper
	static server and remove this view.
	"""
	logo_path = os.path.join(settings.BASE_DIR, 'core', 'images', 'logo.jpg')
	if not os.path.exists(logo_path):
		raise Http404('Logo not found')
	return FileResponse(open(logo_path, 'rb'), content_type='image/jpeg')


def subject_list(request):
	"""Display list of subjects with search and pagination similar to students list.

	Supports simple name search via ?q= and pagination (20 per page).
	"""
	q = request.GET.get('q', '').strip()
	subjects = Subject.objects.all().order_by('-created_at')
	if q:
		subjects = subjects.filter(name__icontains=q)

	paginator = Paginator(subjects, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'q': q,
		'page_obj': page_obj,
	}
	return render(request, 'core/subject_list.html', context)


def subject_create(request):
	"""Create a new Subject (مضمون)."""
	if request.method == 'POST':
		form = SubjectForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'مضمون با موفقیت ثبت شد.')
			return redirect(reverse('core:subject_list'))
	else:
		form = SubjectForm()
	return render(request, 'core/subject_form.html', {'form': form})


def subject_edit(request, pk):
	"""Edit an existing Subject."""
	subject = get_object_or_404(Subject, pk=pk)
	if request.method == 'POST':
		form = SubjectForm(request.POST, instance=subject)
		if form.is_valid():
			form.save()
			messages.success(request, 'اطلاعات مضمون با موفقیت بروزرسانی شد.')
			return redirect(reverse('core:subject_list'))
	else:
		form = SubjectForm(instance=subject)
	return render(request, 'core/subject_form.html', {'form': form})


def subject_delete(request, pk):
	"""Delete a Subject (POST only to perform deletion)."""
	subject = get_object_or_404(Subject, pk=pk)
	if request.method == 'POST':
		subject.delete()
		messages.success(request, 'مضمون حذف شد.')
		return redirect(reverse('core:subject_list'))
	return render(request, 'core/class_confirm_delete.html', {'klass': subject})


def classes_list(request):
	"""Display list of classes with search and pagination similar to students list.

	If there is no SchoolClass data yet, the page will show empty state (and the
	"+ افزودن صنف جدید" button still allows creating new classes).
	"""
	q = request.GET.get('q', '').strip()
	classes = SchoolClass.objects.all().order_by('-created_at')
	if q:
		classes = classes.filter(name__icontains=q)

	paginator = Paginator(classes, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'q': q,
		'page_obj': page_obj,
	}
	return render(request, 'core/classes_list.html', context)


def class_create(request):
	"""Create a new SchoolClass."""
	if request.method == 'POST':
		form = SchoolClassForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'صنف با موفقیت ثبت شد.')
			return redirect(reverse('core:classes_list'))
	else:
		form = SchoolClassForm()
	return render(request, 'core/class_form.html', {'form': form})


def class_edit(request, pk):
	"""Edit an existing SchoolClass."""
	klass = get_object_or_404(SchoolClass, pk=pk)
	if request.method == 'POST':
		form = SchoolClassForm(request.POST, instance=klass)
		if form.is_valid():
			form.save()
			messages.success(request, 'اطلاعات صنف با موفقیت بروزرسانی شد.')
			return redirect(reverse('core:classes_list'))
	else:
		form = SchoolClassForm(instance=klass)
	return render(request, 'core/class_form.html', {'form': form})


def class_delete(request, pk):
	"""Delete a SchoolClass. Accept POST only to perform deletion."""
	klass = get_object_or_404(SchoolClass, pk=pk)
	if request.method == 'POST':
		klass.delete()
		messages.success(request, 'صنف حذف شد.')
		return redirect(reverse('core:classes_list'))
	return render(request, 'core/class_confirm_delete.html', {'klass': klass})


def student_edit(request, pk):
	"""Edit an existing student."""
	student = get_object_or_404(Student, pk=pk)
	if request.method == 'POST':
		form = StudentForm(request.POST, request.FILES, instance=student)
		if form.is_valid():
			form.save()
			messages.success(request, 'اطلاعات دانش‌آموز با موفقیت بروزرسانی شد.')
			return redirect(reverse('core:student_list'))
	else:
		form = StudentForm(instance=student)
	class_names = list(SchoolClass.objects.values_list('name', flat=True))
	return render(request, 'core/student_form_clean.html', {'form': form, 'class_names': class_names})


def student_delete(request, pk):
	"""Delete a student. Only accept POST to perform deletion."""
	student = get_object_or_404(Student, pk=pk)
	if request.method == 'POST':
		student.delete()
		messages.success(request, 'دانش‌آموز حذف شد.')
		return redirect(reverse('core:student_list'))
	# If GET, render a very small confirmation page (fallback) to avoid accidental deletes
	return render(request, 'core/student_confirm_delete.html', {'student': student})


def dashboard(request):
	"""Dashboard view showing totals and a pie chart of students per class."""
	total_students = Student.objects.count()
	total_teachers = Teacher.objects.count()
	total_subjects = Subject.objects.count()
	total_classes = SchoolClass.objects.count()

	# Prepare data for pie chart: count of students per SchoolClass name.
	classes = list(SchoolClass.objects.order_by('name'))
	labels = [c.name for c in classes]
	counts = [Student.objects.filter(class_name=c.name).count() for c in classes]

	# If there are no defined classes but some students have class_name values,
	# fall back to grouping by student.class_name values.
	if not classes:
		from django.db.models import Count
		qs = Student.objects.values('class_name').annotate(cnt=Count('id')).order_by('-cnt')
		labels = [x['class_name'] or 'نامشخص' for x in qs]
		counts = [x['cnt'] for x in qs]

	chart_json = mark_safe(json.dumps({'labels': labels, 'data': counts}))

	context = {
		'total_students': total_students,
		'total_teachers': total_teachers,
		'total_subjects': total_subjects,
		'total_classes': total_classes,
		'chart_json': chart_json,
	}
	return render(request, 'core/dashboard.html', context)
