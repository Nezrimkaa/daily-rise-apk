# Dockerfile для сборки Daily Rise APK
FROM ghcr.io/kivy/buildozer:latest

# Устанавливаем лицензии Android SDK
RUN mkdir -p /home/user/.android/licenses && \
    echo "8933bad161af4178b1185d1a37fbf41ea5269c55" > /home/user/.android/licenses/android-sdk-license && \
    echo "d56f5187479451eabf01fb78af6dfcb131a6481e" >> /home/user/.android/licenses/android-sdk-license && \
    echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" >> /home/user/.android/licenses/android-sdk-license

# Рабочая директория
WORKDIR /home/user/app

# Копируем файлы проекта
COPY android-app/ /home/user/app/

# Запускаем сборку
CMD ["buildozer", "android", "debug"]
