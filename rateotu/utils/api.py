class ReadWriteSerializerMixin:
    """
    Overrides get_serializer_class to choose the read serializer
    for GET method (HEAD, OPTIONS are handled by 'metadata_class')
    and the write serializer for unsafe (POST, PUT, PATCH) http methods.

    Usage: set read_serializer_class and write_serializer_class attributes
    on a 'generics' APIView subclass which can accept multiple methods
    (e.g. GET AND POST).
    """

    read_serializer_class = None
    write_serializer_class = None

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return self.get_write_serializer_class()
        return self.get_read_serializer_class()

    def get_read_serializer_class(self):
        assert self.read_serializer_class is not None, (
            "'%s' should either include a `read_serializer_class` attribute,"
            "or override the `get_read_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.read_serializer_class

    def get_write_serializer_class(self):
        assert self.write_serializer_class is not None, (
            "'%s' should either include a `write_serializer_class` attribute,"
            "or override the `get_write_serializer_class()` method."
            % self.__class__.__name__
        )
        return self.write_serializer_class
