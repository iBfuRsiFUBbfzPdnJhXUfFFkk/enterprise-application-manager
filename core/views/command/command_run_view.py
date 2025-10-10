import subprocess
import sys
from typing import Mapping, Any
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST

from core.models.command import Command
from core.views.generic.generic_500 import generic_500


@require_POST
def command_run_view(request: HttpRequest, model_id: int) -> JsonResponse:
    """
    Execute a Python command safely with timeout and output capture.
    Only allows Python commands to be executed.
    """
    try:
        command = Command.objects.get(id=model_id)
    except Command.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Command not found'
        }, status=404)

    # Only allow Python commands to be executed
    if not command.is_python():
        return JsonResponse({
            'success': False,
            'error': f'Only Python commands can be executed. This command is marked as: {command.get_language_display()}'
        }, status=400)

    try:
        # Execute the Python command with a timeout
        # Use subprocess for better security and output capture
        result = subprocess.run(
            [sys.executable, '-c', command.command],
            capture_output=True,
            text=True,
            timeout=30,  # 30 second timeout
            check=False  # Don't raise exception on non-zero exit
        )

        # Prepare response
        response_data: Mapping[str, Any] = {
            'success': True,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'return_code': result.returncode,
            'command_name': command.name,
        }

        return JsonResponse(response_data)

    except subprocess.TimeoutExpired:
        return JsonResponse({
            'success': False,
            'error': 'Command execution timed out (30 second limit)'
        }, status=408)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Execution error: {str(e)}'
        }, status=500)
