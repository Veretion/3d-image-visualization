#  Кроме того, что требуется установка библиотек, данный пример должен работать из коробки
#  Размер фотографии очень сильно влияет на объём отрисовки, загружает видеокарту
#  При слабой видеокарте рекомендуемый размер изображения 200 - 500 кб, при средней 500 - 1мб
#  Настройки чуть ниже, кроме того, ещё ниже, есть возможность самостоятельной регулировки относительного размера отображаемого графика, не рекомендуется

import numpy as np
from PIL import Image
import plotly.graph_objs as go


image_path = 'example.png'  # название фотографии
scale_factor = 1  # по необходимости, в зависимости от вычислительной мощности и разрешения исходного изображения изменяем, рекомендуемый диапазон от 1 до 0.01
x_size_graf = 1600  # влияет на размер окна отображения графика, ширина окна
y_size_graf = 1200  # высота окна, оба параметра не влияют на сам график


def load_and_resize_image(image_path, scale_factor=0.5):
    """
    Загружает изображение, преобразует его в RGB и при необходимости изменяет разрешение.

    :param image_path: путь к изображению
    :param scale_factor: коэффициент масштабирования (по умолчанию 0.5)
    :return: изображение в виде массива numpy с типом float32
    """
    image = Image.open(image_path).convert('RGB')
    if scale_factor != 1.0:
        new_size = (int(image.width * scale_factor), int(image.height * scale_factor))
        image = image.resize(new_size)
    return np.array(image, dtype=np.float32)


def prepare_image_channels(image_array):
    """
    Подготавливает координаты и нормализованные каналы изображения.

    :param image_array: массив изображения в формате (height, width, channels)
    :return: кортеж (x, y, z_red, z_green, z_blue, height, width)
    """
    height, width, _ = image_array.shape
    # Создаём координатную сетку: инвертируем ось X для соответствия оригинальному виду
    x, y = np.meshgrid(np.arange(width)[::-1], np.arange(height))
    # Нормализуем значения каналов в диапазоне [0, 1]
    z_red = image_array[:, :, 0] / 255.0
    z_green = image_array[:, :, 1] / 255.0
    z_blue = image_array[:, :, 2] / 255.0
    return x, y, z_red, z_green, z_blue, height, width


def create_3d_plot(x, y, z_channels, height, width):
    """
    Создаёт 3D-график для каждого цветового канала с использованием Plotly.

    :param x: координаты X
    :param y: координаты Y
    :param z_channels: кортеж из массивов для красного, зелёного и синего каналов
    :param height: высота изображения
    :param width: ширина изображения
    :return: объект Figure от Plotly
    """
    fig = go.Figure()
    colors = ['red', 'green', 'blue']
    names = ['Red Channel', 'Green Channel', 'Blue Channel']

    for z, color, name in zip(z_channels, colors, names):
        fig.add_trace(go.Scatter3d(
            x=x.flatten(),
            y=y.flatten(),
            z=z.flatten(),
            mode='markers',
            marker=dict(size=2, color=color),
            name=name
        ))

    fig.update_layout(
        width=x_size_graf,  # 
        height=y_size_graf,
        scene=dict(
            xaxis_title='X (Width)',
            yaxis_title='Y (Height)',
            zaxis_title='Intensity',
            aspectmode='manual',  # позволяет выставить настройки вручную, для автоматической настройки необходимо закомментировать эту и нижнюю строки
            aspectratio=dict(x=10, y=(height / width) * 10, z=4)  # изминяет относительные размеры графика, по умолчанию можно поставить везде 10
        )
    )
    return fig


def main():
 
    # Загрузка и предобработка изображения
    image_array = load_and_resize_image(image_path, scale_factor)
    x, y, z_red, z_green, z_blue, height, width = prepare_image_channels(image_array)

    # Создание 3D-графика
    fig = create_3d_plot(x, y, (z_red, z_green, z_blue), height, width)
    fig.show()


if __name__ == '__main__':
    main()
