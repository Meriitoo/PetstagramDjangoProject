def megabytes_to_bytes(mb):
    return mb * 1024 * 1024


def is_owner(request, obj):
    return request.user == obj.user

# We can do mixin for all methods, when something is repeating, like function, like forms DisabledFormMixin in core folder
# class OwnerRequired:
#     def get(self, request, *args, **kwargs):
#         result = super().get(request, *args, **kwargs)
#
#         if request.user == self.object.user:
#             return result
#         else:
#             return '...'
#
#     def post(....)
