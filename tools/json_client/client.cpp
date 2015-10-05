#include "client.h"


void Client::replyFinished(QNetworkReply *reply)
{
    QByteArray rawData = reply->readAll();
    QJsonDocument doc(QJsonDocument::fromJson(rawData));
    QJsonObject json = doc.object();
    qDebug() << "Temperature: " << json["temperature"];
    qDebug() << "Humidity: " << json["humidity"];
    qDebug() << "Time: " << json["at"];
}

void Client::GetJsonString(QString url)
{
    QUrl qrl(url);
    manager = new QNetworkAccessManager(this);
    connect(manager, SIGNAL(finished(QNetworkReply*)), this, SLOT(replyFinished(QNetworkReply*)));
    manager->get(QNetworkRequest(qrl));
}

Client::~Client()
{
    delete manager;
}
