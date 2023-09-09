import requests
from .connect import Connect


class Handler(Connect):
    delivery_service_href = 'https://api.moysklad.ru/api/remap/1.2/entity/service/1892e040-4e54-11ee-0a80-10c2001267b3'
    previous_orders = {}

    def create_delivery(self, order):
        order_id = order['id']
        total_param = self.get_volume_and_weight(order)
        volume = total_param[0]
        weight = total_param[1]

        order_position_data = {
            'quantity': 1,
            'price': weight/volume*500.0,
            'assortment': {
                'meta': {
                    'href': self.delivery_service_href,
                    'type': 'service'
                }
            }
        }
        print(f'бъем= {volume} | вес= {weight} | total= {weight / volume * 500}')
        response = requests.post(f'{self.url}/{order_id}/positions', headers=self.headers,
                                 json=order_position_data)

    def get_volume_and_weight(self, order):
        order_id = order['id']
        order_positions_url = f'{self.url}/{order_id}/positions'

        try:
            response = requests.get(order_positions_url, headers=self.headers)
            current_orders = {order['id']: order for order in response.json()['rows']}

            total_volume = 0
            total_weight = 0

            for key, val in current_orders.items():
                tmp_url = val['assortment']['meta']['href']
                item_response = requests.get(tmp_url, headers=self.headers).json()
                item_volume = item_response.get('volume', 0)
                item_weight = item_response.get('weight', 0)
                total_volume += float(item_volume)
                total_weight += float(item_weight)
                print(total_volume)

            total_param = [total_volume, total_weight]
            return total_param

        except requests.exceptions.RequestException as e:
            print(f'Ошибка при получении информации о заказе {order_id}: {str(e)}')
            return None

    def site_monitor(self):
        response = self.index()
        current_orders = {order['id']: order for order in response.json()['rows']}

        for order_id, order in current_orders.items():
            if order_id not in self.previous_orders:
                print(f'Заказ создан: {order["id"]}')
                self.create_delivery(order)

            self.previous_orders = current_orders