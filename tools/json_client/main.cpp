#include <QCoreApplication>
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <client.h>

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    Client c;
    c.GetJsonString("http://0.0.0.0:6543/current.json");
    return a.exec();
}
