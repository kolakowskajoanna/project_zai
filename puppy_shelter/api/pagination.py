from typing import Optional
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def get_page_number(link: Optional[str]) -> Optional[int]:
    if link is None: return None  # ! jesli nie ma urla to oddajemy null
    try: return int(link[(link.find('page=') + 5): len(link)])
    except Exception: return None # ! ^ nie ma page=


class PuppyPagination(PageNumberPagination):
    def get_paginated_response(self, data):

        return Response({
            'pagination': {
                'next': get_page_number(self.get_next_link()),
                'prev':get_page_number(self.get_previous_link()),
                'total': self.page.paginator.count
            },
            'results': data
        })
