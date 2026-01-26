from busca.app.bootstrap import bootstrap


def main():
    container = bootstrap()

    service = container.nota_ri_sync_service()
    stats = service.sync()

    print(stats)


if __name__ == '__main__':
    main()