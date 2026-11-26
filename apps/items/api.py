from django.db.models import QuerySet
from django.http import Http404, HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router, Status
from ninja.pagination import LimitOffsetPagination, paginate

from apps.items.models import Item
from apps.items.schemas import ItemIn, ItemOut, ItemPatch

router = Router(tags=["items"])


@router.get("", response=list[ItemOut])
@paginate(LimitOffsetPagination)
def list_items(request: HttpRequest) -> QuerySet[Item]:
    return Item.objects.all()


@router.post("", response={201: ItemOut})
def create_item(request: HttpRequest, payload: ItemIn) -> Status[Item]:
    return Status(201, Item.objects.create(**payload.model_dump()))


@router.get("/{item_id}", response=ItemOut)
def get_item(request: HttpRequest, item_id: int) -> Item:
    return get_object_or_404(Item, id=item_id)


@router.patch("/{item_id}", response=ItemOut)
def update_item(request: HttpRequest, item_id: int, payload: ItemPatch) -> Item:
    item = get_object_or_404(Item, id=item_id)
    changes = payload.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in changes.items():
        setattr(item, field, value)
    item.save(update_fields=[*changes, "updated_at"])
    return item


@router.delete("/{item_id}", response={204: None})
def delete_item(request: HttpRequest, item_id: int) -> Status[None]:
    deleted, _ = Item.objects.filter(id=item_id).delete()
    if not deleted:
        raise Http404
    return Status(204, None)
