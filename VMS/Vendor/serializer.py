from rest_framework import serializers
from .models import (
    VendorProfile,
    HistoricalPerformance
)


class VendorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ["id",
                  "name",
                  "vendor_code"]


class VendorDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ["id",
                  "name",
                  "contact_details",
                  "address",
                  "vendor_code"]


class VendorMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ["id",
                  "name",
                  "vendor_code",
                  "on_time_delivery_rate",
                  "quality_rating_avg",
                  "average_response_time",
                  "fulfillment_rate"]


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = ["id",
                  "vendor",
                  "date",
                  "on_time_delivery_rate",
                  "quality_rating_avg",
                  "average_response_time",
                  "fulfillment_rate"]
