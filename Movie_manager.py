def main():
    favourite_movie = set()
    while True:
        print("\n--- WELCOME TO THE PROGAM ---")
        print("\n--- Favorite Movies Manager ---")
        print("1. View your Favourite Movies.")
        print("2. Add your Favourite Movie.")
        print("3. Remove the movie from the list.")
        print("4. Exit")

        choice = input ("Enter your opton from 1 to 4:")

        if choice == '1':
            if favourite_movie:
                print("---Favourite Movie List---")
                for movie in favourite_movie:
                    print(f"{movie}", sep="\n")
            else:
                print("No movies to display")

        elif choice == '2':
            try:
                n = int(input("Enter number of movies you want to add: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            for _ in range(n):
                favourite_movie.add(input("Enter movie you want to add in list: "))
            print("Movies added successfully!")

        elif choice == '3':

            movie = input(" Enter movie you want to remove: ")
            if movie in favourite_movie:
                favourite_movie.remove(movie)
                print(f"{movie} has been removed successfully !")
            else:
                print("Movie is not present in list!")

        elif choice == '4':
            print ("Exiting the Program....Goodbye!!!") 
            break

        else:
            print("Invalid Input....")

if __name__ == "__main__":
    main()
    