from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import colorama as Color


def Connect_to_db_mongo(
    uri="mongodb+srv://olegniedz:Oleg77918082@cluster0.swjmkbh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
):
    # Create a new db_connection and connect to the server
    db_connection = MongoClient(uri, server_api=ServerApi("1"))
    # Send a ping to confirm a successful connection
    try:
        db_connection.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return db_connection
    except Exception as e:
        print(e)
        return None


def db_document_create(db_collection, kwargs={}):
    result = None
    if kwargs["name"] and len(list(db_collection.find({"name": kwargs["name"]}))) == 0:
        result = db_collection.insert_one(kwargs)
        if result:
            print(f"{result} - Successfully added to MongoDB!")
    return result


def db_document_read(db_collection, name=""):
    if name:
        try:
            result = db_collection.find_one({"name": name})
            for k, v in result.items():
                print(f"{Color.Fore.LIGHTYELLOW_EX}{k, v}{Color.Fore.RESET}")
            return result
        except Exception as e:
            print(e)
    else:
        try:
            results = db_collection.find()
            for result in results:
                print(
                    f"{Color.Fore.LIGHTWHITE_EX}-------------------------------------{Color.Fore.RESET}"
                )
                for k, v in result.items():
                    print(f"{Color.Fore.LIGHTYELLOW_EX}{k, v}{Color.Fore.RESET}")
            return results
        except Exception as e:
            print(e)


def db_document_update(db_collection, old_name, kwargs):

    if kwargs["name"] and len(list(db_collection.find({"name": kwargs["name"]}))) == 0:
        try:
            result = db_collection.update_one(
                {"name": kwargs["name"]}, {"$set": kwargs}
            )
            if result:
                print(f"{result} - Successfully updated in MongoDB!")
            return result
        except Exception as e:
            print(e)


def db_document_delete(db_collection, name=""):
    if name:
        try:
            result = db_collection.find_one_and_delete({"name": name})
        except Exception as e:
            print(e)
    else:
        try:
            results = db_collection.delete_many()
            for result in results:
                print(result)
        except Exception as e:
            print(e)


def main():
    uri = "mongodb+srv://olegniedz:Oleg77918082@cluster0.swjmkbh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    db_connection = Connect_to_db_mongo(uri=uri)

    if db_connection:
        db_collection = db_connection.ds02.cats
        Color.init(autoreset=True)
        comands = {
            "add": "create a new cat",
            "change": "change the cat by name",
            "show": "show cat",
            "remove": "remove cat",
            "exit": "exit",
        }

        def build_kwargs(name: str, age: int, features: list):
            return {"name": name, "age": age, "features": features}

        def promt(
            msg_promt: str,
            variants: tuple = (),
            msg_err="",
            ignore_caps=False,
            allow_empty=False,
        ):
            while True:
                answer = input(f"{Color.Fore.LIGHTBLUE_EX} {msg_promt}{Color.Fore.RED}")
                if allow_empty and not answer:
                    break
                if ignore_caps:
                    answer = answer.lower()
                if answer and not variants or answer in variants:
                    break
                else:
                    print(msg_err)
            return answer

        for command in comands:
            print(
                f"{Color.Fore.LIGHTGREEN_EX}{command:20} - {comands[command]}{Color.Fore.RESET}"
            )

        while True:
            command = promt(
                "Enter command:", tuple(comands.keys()), "Unknown command!", True
            )
            match command:
                case "add":
                    name = promt("Enter name: ")
                    age = promt("Enter age (from 1 to 25): ", tuple(range(1, 25)))
                    features = []
                    feature = "_"
                    while feature:
                        feature = promt(
                            "Enter feature (empty for cancel): ", allow_empty=True
                        )
                        features.append(feature)
                        print(f"features: {features}")
                    if name and age:
                        db_document_create(
                            db_collection=db_collection,
                            kwargs=build_kwargs(name, age, features),
                        )

                case "change":
                    find_name = promt("Enter name: ")
                    cat = db_collection.find_one({"name": find_name})
                    if cat:
                        name = promt(
                            f"name ={cat.name}; Enter new name (empty without change): ",
                            allow_empty=True,
                        )
                        age = promt(
                            f"age ={cat.age}; Enter new age (from 1 to 25) (empty without change): ",
                            tuple(range(1, 25)),
                            allow_empty=True,
                        )
                        features = []
                        feature = promt(
                            f"features ={cat.features}; Enter new features (empty without change): ",
                            allow_empty=True,
                        )
                        while feature:
                            feature = promt(
                                "Enter feature (empty for end): ", allow_empty=True
                            )
                            features.append(feature)
                            print(f"features: {features}")
                        name = name if name else cat.name
                        age = age if age else cat.age
                        features = features if features else cat.features

                        if name and age:
                            db_document_update(
                                db_collection=db_collection,
                                kwargs=build_kwargs(name, age, features),
                                old_name=cat.name,
                            )

                case "show":
                    db_document_read(
                        db_collection=db_collection,
                        name=promt(
                            "Enter name (empty for all cats): ", allow_empty=True
                        ),
                    )

                case "remove":
                    db_document_delete(
                        db_collection=db_collection,
                        name=promt(
                            "Enter name (empty for all cats): ", allow_empty=True
                        ),
                    )

                case "exit":
                    print("\nGood bye!\n")
                    break
                case _:
                    print("Invalid command!\n")

        # db_collection = db_connection.ds02.cats
        # kwargs = {
        #     "name": "basyl",
        #     "age": 4,
        #     "features": ["ходить в капцях", "дає себе гладити", "сірий"],
        # }
        # db_document_create(db_collection=db_collection,kwargs=kwargs)


if __name__ == "__main__":
    main()
