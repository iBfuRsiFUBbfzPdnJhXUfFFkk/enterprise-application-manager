#!/usr/bin/env python3
"""
Script to generate templates for all models following the application pattern
"""

import os
from pathlib import Path

# Model configurations with their specific fields and settings
MODELS_CONFIG = {
    'Requirement': {
        'app_name': 'requirement',
        'color': 'indigo',
        'plural': 'Requirements',
        'description': 'Manage system and security requirements',
        'icon_path': 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4',
        'fields': {
            'name': {'type': 'text', 'label': 'Name', 'required': True, 'tooltip': 'The name of the requirement'},
            'comment': {'type': 'textarea', 'label': 'Comment', 'required': False, 'tooltip': 'Additional details about this requirement'},
            'applications': {'type': 'm2m', 'label': 'Applications', 'required': False, 'tooltip': 'Applications this requirement applies to'},
            'is_for_soc': {'type': 'boolean', 'label': 'SOC Requirement', 'required': False},
            'is_for_spsrd': {'type': 'boolean', 'label': 'SPSRD Requirement', 'required': False},
            'is_functional_requirement': {'type': 'boolean', 'label': 'Functional Requirement', 'required': False},
        },
        'sections': [
            {'name': 'Basic Information', 'fields': ['name', 'comment']},
            {'name': 'Associations', 'fields': ['applications']},
            {'name': 'Requirement Flags', 'fields': ['is_for_soc', 'is_for_spsrd', 'is_functional_requirement']},
        ]
    },
    # Add more models as needed
}

def generate_list_template(model_name, config):
    """Generate list template with grid/list view"""
    app_name = config['app_name']
    plural = config['plural']
    color = config['color']
    description = config['description']
    icon_path = config['icon_path']

    # Determine search fields (name and acronym if present)
    search_fields = ['name']
    if 'acronym' in config['fields']:
        search_fields.append('acronym')

    template = f"""{{%extends 'authenticated/base_authenticated.html' %}}
{{% block content %}}
<div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div class="flex justify-between items-center">
                <div>
                    <h1 class="text-3xl font-bold text-gray-900">{plural}</h1>
                    <p class="mt-1 text-sm text-gray-500">{description}</p>
                </div>
                <a href="{{% url '{app_name}_new' %}}"
                   class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-lg text-white bg-{color}-600 hover:bg-{color}-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-{color}-500 transition-all duration-200">
                    <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                    </svg>
                    New {model_name}
                </a>
            </div>
        </div>
    </div>

    <!-- Search and Filters -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <!-- Search -->
                <div>
                    <label for="search-input" class="block text-sm font-medium text-gray-700 mb-1">Search</label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                            </svg>
                        </div>
                        <input type="text" id="search-input" placeholder="Search by {' or '.join(search_fields)}..."
                               class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-{color}-500 focus:border-{color}-500 sm:text-sm">
                    </div>
                </div>
            </div>

            <!-- View Toggle and Count -->
            <div class="mt-4 flex justify-between items-center">
                <div class="text-sm text-gray-700">
                    Showing <span id="visible-count" class="font-medium">0</span> of <span id="total-count" class="font-medium">{{{{ models|length }}}}</span> {plural.lower()}
                </div>
                <div class="flex items-center space-x-2">
                    <span class="text-sm text-gray-700">View:</span>
                    <button id="view-grid" onclick="setView('grid')"
                            class="p-2 text-gray-400 hover:text-gray-600 focus:outline-none">
                        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
                        </svg>
                    </button>
                    <button id="view-list" onclick="setView('list')"
                            class="p-2 text-{color}-600 hover:text-{color}-800 focus:outline-none">
                        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Grid View -->
        <div id="grid-view" class="hidden grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {{% for model in models %}}
            <div class="{app_name}-card bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200"
                 data-name="{{{{ model.name|lower }}}}"
                 {'data-acronym="{{{{ model.acronym|default:\\'\\' |lower }}}}"' if 'acronym' in config['fields'] else ''}>
                <div class="p-6">
                    <!-- Header -->
                    <div class="flex justify-between items-start mb-4">
                        <div class="flex-1">
                            <div class="flex items-center space-x-2">
                                <svg class="h-6 w-6 text-{color}-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{icon_path}"/>
                                </svg>
                                <h3 class="text-lg font-semibold text-gray-900">{{{{ model.name|default:"—" }}}}</h3>
                            </div>
                        </div>
                    </div>

                    <!-- Comment Preview -->
                    {{% if model.comment %}}
                    <div class="mb-4">
                        <p class="text-sm text-gray-500 line-clamp-3">{{{{ model.comment|truncatewords:20 }}}}</p>
                    </div>
                    {{% endif %}}

                    <!-- Actions -->
                    <div class="flex justify-between items-center pt-4 border-t border-gray-200">
                        <a href="{{% url '{app_name}_detail' model_id=model.id %}}"
                           class="text-sm font-medium text-{color}-600 hover:text-{color}-800">
                            View Details →
                        </a>
                        <div class="flex space-x-2">
                            <a href="{{% url '{app_name}_edit' model_id=model.id %}}"
                               class="p-1 text-gray-400 hover:text-gray-600"
                               title="Edit">
                                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                                </svg>
                            </a>
                            <button onclick="openDeleteModal('{{{{ model.id }}}}', '{{{{ model.name|escapejs }}}}')"
                                    class="p-1 text-gray-400 hover:text-red-600"
                                    title="Delete">
                                <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            {{% endfor %}}
        </div>

        <!-- List View (simplified) -->
        <div id="list-view" class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                            <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        {{% for model in models %}}
                        <tr class="{app_name}-row hover:bg-gray-50 transition-colors duration-150"
                            data-name="{{{{ model.name|lower }}}}"
                            {'data-acronym="{{{{ model.acronym|default:\\'\\' |lower }}}}"' if 'acronym' in config['fields'] else ''}
                            ondblclick='window.location.href = "{{% url "{app_name}_detail" model_id=model.id %}}"'>
                            <td class="px-4 py-3">
                                <div class="text-sm font-medium text-gray-900">{{{{ model.name|default:"—" }}}}</div>
                            </td>
                            <td class="px-4 py-3 whitespace-nowrap text-center">
                                <div class="flex justify-center space-x-2">
                                    <a href="{{% url '{app_name}_detail' model_id=model.id %}}"
                                       class="text-blue-600 hover:text-blue-900" title="View">
                                        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                                        </svg>
                                    </a>
                                    <a href="{{% url '{app_name}_edit' model_id=model.id %}}"
                                       class="text-gray-600 hover:text-gray-900" title="Edit">
                                        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                                        </svg>
                                    </a>
                                    <button onclick="openDeleteModal('{{{{ model.id }}}}', '{{{{ model.name|escapejs }}}}')"
                                            class="text-red-600 hover:text-red-900" title="Delete">
                                        <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                                        </svg>
                                    </button>
                                </div>
                            </td>
                        </tr>
                        {{% endfor %}}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Empty State -->
        <div id="empty-state" class="hidden bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="{icon_path}"/>
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">No {plural.lower()} found</h3>
            <p class="mt-1 text-sm text-gray-500">Try adjusting your search or create a new {model_name.lower()}</p>
        </div>
    </div>
</div>

<!-- Delete Confirmation Modal -->
<div id="deleteModal" class="hidden fixed z-50 inset-0 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onclick="closeDeleteModal()"></div>
        <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div class="sm:flex sm:items-start">
                    <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                        <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                        </svg>
                    </div>
                    <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                        <h3 class="text-lg leading-6 font-medium text-gray-900">Delete {model_name}</h3>
                        <div class="mt-2">
                            <p class="text-sm text-gray-500">
                                Are you sure you want to delete <strong id="deleteItemName"></strong>? This action cannot be undone.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                <form id="deleteForm" method="POST" action="">
                    {{% csrf_token %}}
                    <button type="submit" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm">Delete</button>
                </form>
                <button type="button" onclick="closeDeleteModal()" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-{color}-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">Cancel</button>
            </div>
        </div>
    </div>
</div>

<script>
let currentView = 'list';

document.addEventListener('DOMContentLoaded', function() {{
    setView(localStorage.getItem('eam_{app_name}_view') || 'list');
    document.getElementById('search-input').addEventListener('input', filter{plural});
    filter{plural}();
}});

function setView(view) {{
    currentView = view;
    localStorage.setItem('eam_{app_name}_view', view);
    const gridView = document.getElementById('grid-view');
    const listView = document.getElementById('list-view');
    const gridBtn = document.getElementById('view-grid');
    const listBtn = document.getElementById('view-list');

    if (view === 'grid') {{
        gridView.classList.remove('hidden');
        listView.classList.add('hidden');
        gridBtn.classList.add('text-{color}-600');
        gridBtn.classList.remove('text-gray-400');
        listBtn.classList.add('text-gray-400');
        listBtn.classList.remove('text-{color}-600');
    }} else {{
        gridView.classList.add('hidden');
        listView.classList.remove('hidden');
        listBtn.classList.add('text-{color}-600');
        listBtn.classList.remove('text-gray-400');
        gridBtn.classList.add('text-gray-400');
        gridBtn.classList.remove('text-{color}-600');
    }}
    filter{plural}();
}}

function filter{plural}() {{
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const cards = document.querySelectorAll('.{app_name}-card');
    const rows = document.querySelectorAll('.{app_name}-row');
    const items = currentView === 'grid' ? cards : rows;
    let visibleCount = 0;

    items.forEach(item => {{
        const name = item.dataset.name || '';
        {'const acronym = item.dataset.acronym || \\'\\';' if 'acronym' in config['fields'] else ''}
        const matchesSearch = !searchTerm || name.includes(searchTerm){'|| acronym.includes(searchTerm)' if 'acronym' in config['fields'] else ''};

        if (matchesSearch) {{
            item.style.display = '';
            visibleCount++;
        }} else {{
            item.style.display = 'none';
        }}
    }});

    document.getElementById('visible-count').textContent = visibleCount;
    const emptyState = document.getElementById('empty-state');
    if (visibleCount === 0) {{
        emptyState.classList.remove('hidden');
        document.getElementById('grid-view').classList.add('hidden');
        document.getElementById('list-view').classList.add('hidden');
    }} else {{
        emptyState.classList.add('hidden');
        if (currentView === 'grid') {{
            document.getElementById('grid-view').classList.remove('hidden');
        }} else {{
            document.getElementById('list-view').classList.remove('hidden');
        }}
    }}
}}

function openDeleteModal(id, name) {{
    document.getElementById('deleteItemName').textContent = name;
    document.getElementById('deleteForm').action = "{{% url '{app_name}_delete' model_id=0 %}}".replace('/0/', '/' + id + '/');
    document.getElementById('deleteModal').classList.remove('hidden');
}}

function closeDeleteModal() {{
    document.getElementById('deleteModal').classList.add('hidden');
}}

document.addEventListener('keydown', function(event) {{
    if (event.key === 'Escape') {{
        closeDeleteModal();
    }}
}});
</script>

<style>
.line-clamp-3 {{
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}}
</style>
{{% endblock %}}
"""
    return template

print("Template generator script ready!")
print("Run this script to generate all templates for the configured models.")
print(f"Configured models: {', '.join(MODELS_CONFIG.keys())}")
