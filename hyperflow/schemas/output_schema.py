from hyperflow.output.base import BaseOutput

# Canonical runtime output model. OutputObject remains as a backward-compatible
# alias for older imports and docs.
OutputObject = BaseOutput

__all__ = ["BaseOutput", "OutputObject"]
