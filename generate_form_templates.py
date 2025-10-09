#!/usr/bin/env python
"""Script to generate custom form templates for remaining models"""
import os

# Define form configurations for each model
FORM_CONFIGS = {
    'dependency': {
        'title': 'Dependency',
        'description': 'software dependency or library',
        'route': 'dependency',
        'sections': [
            {
                'title': 'Dependency Information',
                'description': 'Details about this library or package',
                'fields': [
                    ('name', 'Name', 'The name of the library, package, or dependency', True),
                    ('version', 'Version', 'The version number or tag (e.g., 1.2.3, latest)', False),
                    ('type_programing_concept', 'Type', 'The programming concept or category (Library, Framework, Package, etc.)', False),
                    ('comment', 'Comment', 'Additional notes about this dependency', False, True),
                ]
            }
        ]
    },
    'database': {
        'title': 'Database',
        'description': 'database instance',
        'route': 'database',
        'sections': [
            {
                'title': 'Database Configuration',
                'description': 'Database instance details and settings',
                'fields': [
                    ('application', 'Application', 'The application this database belongs to', False),
                    ('type_environment', 'Environment', 'The environment where this database runs (Development, Staging, Production)', False),
                    ('type_database_flavor', 'Database Flavor', 'The type of database (PostgreSQL, MySQL, MongoDB, etc.)', False),
                    ('version', 'Version', 'The database version number', False),
                    ('type_data_storage_form', 'Storage Model', 'How data is stored (Relational, Document, Key-Value, etc.)', False),
                    ('comment', 'Comment', 'Additional notes about this database instance', False, True),
                ]
            }
        ]
    },
    'document': {
        'title': 'Document',
        'description': 'document or file',
        'route': 'document',
        'sections': [
            {
                'title': 'Document Information',
                'description': 'File and document details',
                'fields': [
                    ('name', 'Name', 'A descriptive name for this document', True),
                    ('blob_filename', 'Filename', 'The actual filename of the uploaded file', False),
                    ('comment', 'Comment', 'Notes or description of this document', False, True),
                ]
            }
        ]
    },
    'secret': {
        'title': 'Secret',
        'description': 'secret credential',
        'route': 'secret',
        'sections': [
            {
                'title': 'Secret Information',
                'description': 'Sensitive credential details',
                'fields': [
                    ('name', 'Name', 'A descriptive name for this secret (e.g., API Key, Database Password)', True),
                    ('comment', 'Comment', 'Purpose or usage notes for this secret', False, True),
                ]
            }
        ]
    },
}

# Template for form HTML
FORM_TEMPLATE = '''{% extends 'authenticated/base_authenticated.html' %}
{% load static %}

{% block content %}
    <!-- Header Section -->
    <div class="bg-white shadow-sm border-b border-gray-200 mb-6">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div class="flex items-center">
                <a href="{% url '{{ROUTE}}' %}" class="mr-4 text-gray-400 hover:text-gray-600 transition-colors duration-150">
                    <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                    </svg>
                </a>
                <div>
                    <h1 class="text-3xl font-bold text-gray-900">{% if form.instance.pk %}Edit{% else %}Create{% endif %} {{TITLE}}</h1>
                    <p class="mt-1 text-sm text-gray-500">{% if form.instance.pk %}Update {{DESCRIPTION}} details{% else %}Add a new {{DESCRIPTION}}{% endif %}</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Form Section -->
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <form method="POST">
            {% csrf_token %}

            <div class="space-y-6">
{{SECTIONS}}
                <!-- Form Actions -->
                <div class="bg-white shadow-md rounded-lg overflow-hidden">
                    <div class="px-6 py-4 bg-gray-50 flex justify-between items-center">
                        <a href="{% url '{{ROUTE}}' %}"
                           class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-150">
                            <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                            </svg>
                            Cancel
                        </a>
                        <button type="submit"
                                class="inline-flex items-center px-6 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-150">
                            <svg class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                            </svg>
                            {% if form.instance.pk %}Update {{TITLE}}{% else %}Create {{TITLE}}{% endif %}
                        </button>
                    </div>
                </div>
            </div>
        </form>
    </div>

    <style>
        /* Style Django form fields with Tailwind */
        input[type="text"],
        input[type="email"],
        input[type="number"],
        input[type="url"],
        input[type="date"],
        input[type="datetime-local"],
        input[type="password"],
        textarea,
        select {
            display: block;
            width: 100%;
            padding: 0.5rem 0.75rem;
            font-size: 0.875rem;
            line-height: 1.5;
            color: #1f2937;
            background-color: #ffffff;
            background-clip: padding-box;
            border: 1px solid #d1d5db;
            border-radius: 0.375rem;
            transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
        }

        input[type="text"]:focus,
        input[type="email"]:focus,
        input[type="number"]:focus,
        input[type="url"]:focus,
        input[type="date"]:focus,
        input[type="datetime-local"]:focus,
        input[type="password"]:focus,
        textarea:focus,
        select:focus {
            color: #1f2937;
            background-color: #ffffff;
            border-color: #3b82f6;
            outline: 0;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        select[multiple] {
            height: 10rem;
            padding: 0.5rem;
        }

        textarea {
            min-height: 100px;
            resize: vertical;
        }

        input[type="checkbox"] {
            width: 1rem;
            height: 1rem;
            color: #3b82f6;
            background-color: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 0.25rem;
            cursor: pointer;
        }

        input[type="checkbox"]:focus {
            border-color: #3b82f6;
            outline: 0;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        input::placeholder,
        textarea::placeholder {
            color: #9ca3af;
            opacity: 1;
        }
    </style>
{% endblock %}
'''

def generate_field_html(field_name, label, tooltip, required=False, is_textarea=False):
    col_span = 'md:col-span-2' if is_textarea else ''
    required_star = '{% if form.' + field_name + '.field.required %}<span class="text-red-500">*</span>{% endif %}' if required else ''

    return f'''                        <div{' class="' + col_span + '"' if col_span else ''}>
                            <label for="{{{{ form.{field_name}.id_for_label }}}}" class="block text-sm font-medium text-gray-700 mb-2 cursor-help" title="{tooltip}">
                                {label} {required_star}
                            </label>
                            {{{{ form.{field_name} }}}}
                            {{% if form.{field_name}.errors %}}<p class="mt-2 text-sm text-red-600">{{{{ form.{field_name}.errors.0 }}}}</p>{{% endif %}}
                        </div>'''

def generate_section_html(section):
    fields_html = []
    for field_info in section['fields']:
        field_name = field_info[0]
        label = field_info[1]
        tooltip = field_info[2]
        required = field_info[3] if len(field_info) > 3 else False
        is_textarea = field_info[4] if len(field_info) > 4 else False
        fields_html.append(generate_field_html(field_name, label, tooltip, required, is_textarea))

    return f'''                <!-- {section['title']} -->
                <div class="bg-white shadow-md rounded-lg overflow-hidden">
                    <div class="px-6 py-4 bg-gray-50 border-b border-gray-200">
                        <h2 class="text-lg font-semibold text-gray-900">{section['title']}</h2>
                        <p class="mt-1 text-sm text-gray-500">{section['description']}</p>
                    </div>
                    <div class="px-6 py-6 grid grid-cols-1 md:grid-cols-2 gap-6">
{chr(10).join(fields_html)}
                    </div>
                </div>
'''

def generate_form_template(config):
    sections_html = '\n'.join([generate_section_html(section) for section in config['sections']])

    template = FORM_TEMPLATE.replace('{{ROUTE}}', config['route'])
    template = template.replace('{{TITLE}}', config['title'])
    template = template.replace('{{DESCRIPTION}}', config['description'])
    template = template.replace('{{SECTIONS}}', sections_html)

    return template

# Generate templates
for model_name, config in FORM_CONFIGS.items():
    template_content = generate_form_template(config)
    template_dir = f'templates/authenticated/{model_name}'
    os.makedirs(template_dir, exist_ok=True)

    template_path = f'{template_dir}/{model_name}_form.html'
    with open(template_path, 'w') as f:
        f.write(template_content)

    print(f'Generated: {template_path}')

print('\nAll form templates generated successfully!')
