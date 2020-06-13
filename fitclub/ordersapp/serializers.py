from rest_framework import serializers
from .models import CalendarDate, TimePeriod, Order, CardItem, ClientCard, Basket

from users.models import ClubClient

class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarDate
        fields = ('id', 'date', )


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimePeriod
        fields = ('id', 'period',)


class BasketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('user', 'date', 'time_period', 'service_id')


class BasketListSerializer(serializers.ModelSerializer):
    date = serializers.ReadOnlyField(source='date.date')
    time_period = serializers.ReadOnlyField(source='time_period.period')
    service_id = serializers.ReadOnlyField(source='service_id.name')
    price = serializers.ReadOnlyField(source='service_id.price')

    class Meta:
        model = Basket
        fields = ('date', 'time_period', 'service_id', 'price')


class BasketOnlyIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('date', 'time_period', 'service_id')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('date', 'time_period', 'service_id', 'quantity')


class CardItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardItem
        fields = ('date', 'time_period', 'service_id')


class ClientCardSerializer(serializers.ModelSerializer):
    card_items = CardItemSerializer(many=True)

    class Meta:
        model = ClientCard
        fields = ('id', 'card_number', 'user', 'card_items')


class CardItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardItem
        fields = ('date', 'time_period', 'service_id')


class ClientCardCreateSerializer(serializers.ModelSerializer):
    card_items = CardItemCreateSerializer(many=True)

    class Meta:
        model = ClientCard
        fields = ('id', 'card_number', 'user', 'card_items', 'client_card_cost')
        #fields = ('id', 'user', 'card_items', 'client_card_cost')

    def create(self, validated_data):
        print(validated_data)
        card_items_dict_list = validated_data.pop('card_items')
        print(card_items_dict_list)
        instance = ClientCard.objects.create(**validated_data)
        for card_items_dict in card_items_dict_list:
            instance.card_items.create(**card_items_dict)

        return instance

    def update(self, instance, validated_data):
        card_items_dict_list = validated_data.pop('card_items', None)

        instance.table_number = validated_data.pop('card_number', instance.card_number)

        instance.save()

        if card_items_dict_list is not None:
            instance.card_items.all().delete()
            for card_items_dict in card_items_dict_list:
                instance.card_items.create(**card_items_dict)

        return instance


class CardItemDetailsSerializer(serializers.ModelSerializer):
    date = serializers.ReadOnlyField(source='date.date')
    time_period = serializers.ReadOnlyField(source='time_period.period')
    service_id = serializers.ReadOnlyField(source='service_id.name')

    class Meta:
        model = CardItem
        fields = ('date', 'time_period', 'service_id')


class ClientCardListSerializer(serializers.ModelSerializer):
    card_items = CardItemDetailsSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ClientCard
        fields = ('id', 'card_number', 'user', 'card_items', 'client_card_cost', 'date_created')


