#ifndef CLIENT_H
#define CLIENT_H

#include <QObject>
#include <QtCore>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QJsonDocument>
#include <QJsonObject>
#include <QByteArray>


class Client: public QObject
{
Q_OBJECT
  QNetworkAccessManager *manager;
private slots:
  void replyFinished(QNetworkReply *);
public:
  void GetJsonString(QString url);
  ~Client();
};


#endif // CLIENT_H
