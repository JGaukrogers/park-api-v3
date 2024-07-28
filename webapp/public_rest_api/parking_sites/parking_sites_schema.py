"""
Copyright 2023 binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from flask_openapi.schema import (
    ArrayField,
    BooleanField,
    DateTimeField,
    DecimalField,
    EnumField,
    IntegerField,
    JsonSchema,
    ObjectField,
    StringField,
    UriField,
)
from parkapi_sources.models.enums import ExternalIdentifierType, PurposeType, SupervisionType

from webapp.models.parking_site import OpeningStatus, ParkAndRideType, ParkingSiteType

parking_site_history_schema = JsonSchema(
    title='ParkingSite',
    properties={
        'id': IntegerField(description='Internal ID, generated by ParkAPI Service.'),
        'static_data_updated_at': DateTimeField(description='Last time static fields were updated. Can be set by the client.'),
        'capacity': IntegerField(minimum=0),
        'capacity_disabled': IntegerField(minimum=0, required=False),
        'capacity_woman': IntegerField(minimum=0, required=False),
        'capacity_family': IntegerField(minimum=0, required=False),
        'capacity_charging': IntegerField(minimum=0, required=False),
        'capacity_carsharing': IntegerField(minimum=0, required=False),
        'capacity_truck': IntegerField(minimum=0, required=False),
        'capacity_bus': IntegerField(minimum=0, required=False),
        'realtime_capacity': IntegerField(minimum=0, required=False),
        'realtime_capacity_disabled': IntegerField(minimum=0, required=False),
        'realtime_capacity_woman': IntegerField(minimum=0, required=False),
        'realtime_capacity_family': IntegerField(minimum=0, required=False),
        'realtime_capacity_charging': IntegerField(minimum=0, required=False),
        'realtime_capacity_carsharing': IntegerField(minimum=0, required=False),
        'realtime_capacity_truck': IntegerField(minimum=0, required=False),
        'realtime_capacity_bus': IntegerField(minimum=0, required=False),
        'realtime_free_capacity': IntegerField(minimum=0, required=False),
        'realtime_free_capacity_disabled': IntegerField(minimum=0, required=False),
        'realtime_free_capacity_woman': IntegerField(minimum=0, required=False),
        'realtime_free_capacity_family': IntegerField(minimum=0, required=False),
        'realtime_free_capacity_charging': IntegerField(minimum=0, required=False),
        'realtime_free_capacity_carsharing': IntegerField(minimum=0, required=False),
        'realtime_free_capacity_truck': IntegerField(minimum=0, required=False),
        'realtime_free_capacity_bus': IntegerField(minimum=0, required=False),
    },
)

parking_site_history_example = {}

parking_site_schema = JsonSchema(
    title='ParkingSite',
    properties={
        'id': IntegerField(description='Internal ID, generated by ParkAPI Service.'),
        'created_at': DateTimeField(description='Creation date in ParkAPI Service database, cannot be set by clients.'),
        'modified_at': DateTimeField(description='Last modified value in ParkAPI Service database, cannot be set by clients.'),
        'source_id': IntegerField(minimum=1, description='Source ID, generated by ParkAPI Service.'),
        'original_uid': StringField(maxLength=256, description='Unique Identifier in original system.'),
        'purpose': EnumField(enum=PurposeType),
        'photo_url': UriField(maxLength=4096, required=False, description='Photo of the parking site'),
        'name': StringField(maxLength=256),
        'operator_name': StringField(maxLength=256, required=False),
        'public_url': UriField(
            maxLength=4096,
            required=False,
            description='URL for human users to get more details about this parking site.',
        ),
        'address': StringField(
            maxLength=512,
            required=False,
            description='Full address including street postalcode and city. Preferable in format <street with number>, <postalcode> <city>',
        ),
        'description': StringField(
            maxLength=4096,
            required=False,
            description='Description for customers like special conditions, remarks how to get there etc.',
        ),
        'type': EnumField(
            enum=ParkingSiteType,
            description='ON_STREET, OFF_STREET_PARKING_GROUND, UNDERGROUND and CAR_PARK are used at car parks, '
            'WALL_LOOPS, STANDS, LOCKERS, SHED, TWO_TIER, BUILDING are used at bike parks, and OTHER at both.',
        ),
        'max_stay': IntegerField(minimum=0, required=False, description='Maximum stay, in seconds.'),
        'max_height': IntegerField(minimum=0, required=False, description='Max height, in centimeters.'),
        'has_lighting': BooleanField(required=False),
        'park_and_ride_type': ArrayField(items=EnumField(enum=ParkAndRideType), required=False),
        'is_supervised': BooleanField(required=False, description='Deprecated, will be replaced by supervision_type.'),
        'supervision_type': EnumField(enum=SupervisionType, required=False),
        'is_covered': BooleanField(required=False),
        'related_location': StringField(maxLength=256, description='A related location like a school.'),
        'has_realtime_data': BooleanField(default=False),
        'fee_description': StringField(required=False),
        'has_fee': BooleanField(required=False),
        'static_data_updated_at': DateTimeField(description='Last time static fields were updated. Can be set by the client.'),
        'realtime_data_updated_at': DateTimeField(
            required=False,
            description='Last time realtime fields were updated. Can be set by the client.',
        ),
        'realtime_opening_status': EnumField(
            enum=OpeningStatus,
            required=False,
            description='Realtime opening status which is reported by the client.',
        ),
        'lat': DecimalField(precision=10, scale=7),
        'lon': DecimalField(precision=10, scale=7),
        'external_identifiers': ArrayField(
            items=ObjectField(
                properties={
                    'type': EnumField(enum=ExternalIdentifierType),
                    'value': StringField(maxLength=256),
                },
            ),
            required=False,
        ),
        'tags': ArrayField(items=StringField(maxLength=256), required=False),
        'opening_hours': StringField(maxLength=512, required=False, description='OSM opening_hours format'),
        **parking_site_history_schema.properties,
    },
)

parking_site_example = {}
