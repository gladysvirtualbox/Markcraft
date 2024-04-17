from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.db.models import Count, Avg, Q , Min, Max 
from django.views.generic import TemplateView 

from .models import  Mark, Student


class DashboardView(TemplateView):
    template_name = 'home_content.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Total counts
        context['total_students'] = Student.objects.count()
        context['total_marks'] = Mark.objects.count()

        # Overall statistics (using aggregation)
        average_mark = Mark.objects.aggregate(Avg('mark'))
        context['average_mark'] = average_mark.get('mark__avg', 0.0)  # Handle potential absence of marks

        highest_mark = Mark.objects.aggregate(Max('mark'))
        context['highest_mark'] = highest_mark.get('mark__max', 0)  # Handle potential absence of marks

        lowest_mark = Mark.objects.aggregate(Min('mark'))
        context['lowest_mark'] = lowest_mark.get('mark__min', 0)  # Handle potential absence of marks

        # Top performing students (using annotations and subqueries)
        # top_students_by_average = (
        #     Student.objects.annotate(average_mark=Avg('marks__mark'))
        #     .order_by('-average_mark')[:5]
        # )
        # context['top_students_by_average'] = top_students_by_average

        # top_students_by_highest_mark = (
        #     Student.objects.annotate(highest_mark=Max('marks__mark'))
        #     .order_by('-highest_mark')[:5]
        # )
        # context['top_students_by_highest_mark'] = top_students_by_highest_mark

        # top_students_by_lowest_mark = (
        #     Student.objects.annotate(lowest_mark=Min('marks__mark'))
        #     .order_by('lowest_mark')[:5]
        # )
        # context['top_students_by_lowest_mark'] = top_students_by_lowest_mark

        # Recent activity
        # context['recent_students'] = Student.objects.order_by('-created_at')[:5]
        # context['recent_marks'] = Mark.objects.order_by('-created_at')[:5]
        print(context)
        return context