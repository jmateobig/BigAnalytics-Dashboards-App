from django.views.generic import  ListView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Category
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from .forms import CategoryForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'category'
    permission_required = 'category.view_category'


class CategoryListJsonView(View):
    def post(self, request, *args, **kwargs):
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '')
        order_column = request.POST.get('order[0][column]', 0)
        order_dir = request.POST.get('order[0][dir]', 'asc')

        # Obtener datos filtrados y ordenados
        categories = Category.objects.all()
        filtered_categories = categories.filter(name__icontains=search_value)
        filtered_categories = categories.filter(Q(name__icontains=search_value) | Q(description__icontains=search_value))

        if order_dir == 'asc':
            order_column_name = request.POST.get(f'columns[{order_column}][data]', 'id')
        else:
            order_column_name = '-' + request.POST.get(f'columns[{order_column}][data]', 'id')

        ordered_categories = filtered_categories.order_by(order_column_name)
        total_records = filtered_categories.count()

        paginated_categories = ordered_categories[start:start + length]

        # Calcular el número de usuarios que tienen el permiso del dashboard
        data = []
        for category in paginated_categories:

            data.append({
                'id': category.id,
                'name': category.name,
                'description': category.description
            })

        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': data,
        }

        return JsonResponse(response)
    

class CategoryDetailJsonView(View):
    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category_id')
        try:
            category = Category.objects.get(pk=category_id)

            # Obtener grupos
            groups_with_category = category.groups.all()

            data = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'groups': list(groups_with_category.values_list('name', flat=True)),
            }

            return JsonResponse({'status': 'success', 'data': data})
        except Category.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Dashboard not found'}, status=404)
        

# class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     model = Category
#     form_class = CategoryForm
#     template_name = 'category_create.html'
#     permission_required = 'category.add_category'
#     success_url = reverse_lazy('category:list')
    

class CategoryEditView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_edit.html'
    success_url = reverse_lazy('category:list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['groups'].initial = self.object.groups.all()
        return form

    def form_valid(self, form):
        return super().form_valid(form)
    

class CategoryDeleteView(View):
    def post(self, request, *args, **kwargs):
        # Obtener el ID de la categoría desde la petición
        category_id = request.POST.get('category_id')

        try:
            # Buscar la categoría, o devolver un error 404 si no existe
            category = get_object_or_404(Category, pk=category_id)

            # Eliminar la relación de la categoría con los grupos
            groups_with_category = Group.objects.filter(category=category)
            for group in groups_with_category:
                group.category = None  # Desasociar el grupo de la categoría
                group.save()

            # Eliminar la categoría
            category.delete()

            return JsonResponse({'status': 'success', 'message': 'Categoría eliminada con éxito'})
        except Category.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Categoría no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)