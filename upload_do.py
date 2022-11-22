import digitalocean


client = digitalocean.get_spaces_client(
    region_name="sgp1",
    endpoint_url="https://countract-space.sgp1.digitaloceanspaces.com",
    key_id="DO00B4LP79TBCTFVXXVJ",
    secret_access_key="5nuWIARIETDnTPbkMblvHI9d6yIlNo7BtPiEiPHsVOk"
)

digitalocean.upload_file_to_space(
    client,
    "images",
    "test.txt",
    "test.txt",
    is_public=True
)