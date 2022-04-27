def get_menu_item_img_dir_upload_path(instance, filename):
    """
    Used to obtain the full upload path after the file has been
    successfuly saved and the MenuItem instance has been created.
    """
    # MEDIA_ROOT/menus/menu-items/images/<name>/<filename>
    return f"menus/menu-items/images/{instance.name.lower()}/{filename}"
