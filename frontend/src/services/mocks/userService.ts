import { User } from "../../types"

let user: User = {
    "username": "bruna",
    "bio": "I am a software developer interested in animes and mangas.",
    "picture": "https://cdn-icons-png.flaticon.com/512/99/99428.png"
}

export const fetchUser = async (username: string): Promise<User> => {
    return new Promise((resolve, reject) => {
        resolve(user)
    })
}
