import { User } from "../../types"

let user: User = {
    "username": "bruna",
    "bio": "I am a software developer interested in animes and mangas.",
    "picture": "https://cdn-icons-png.flaticon.com/512/5968/5968350.png"
}

let users: User[] = [
    {
        "username": "lilith",
        "bio": "I am a cat interested in shoelaces and garbage.",
        "picture": "https://cdn-icons-png.flaticon.com/512/2373/2373010.png"
    },
    {
        "username": "jubs",
        "bio": "I am a dog interested in toys, bones and walks.",
        "picture": "https://cdn-icons-png.flaticon.com/512/8876/8876508.png"
    },
    {
        "username": "ryuk",
        "bio": "I am a god of death interested in apples.",
        "picture": "https://cdn-icons-png.flaticon.com/512/415/415682.png"
    }
]

export const fetchUser = async (username: string): Promise<User> => {
    return new Promise((resolve, reject) => {
        resolve(user)
    })
}

export const changeBio = async (username: string, bio: string) => {
    user.bio = bio
    console.log("Changed bio " + bio)
}

export const changePicture = async (username: string, picture: string) => {
    user.picture = picture
    console.log("Changed picture " + picture)
}

export const changePassword = async (username: string, password: string) => {
    console.log("Changed password " + password)
}

export const login = async (username: string, password: string) => {
    console.log(username + " logged in with password " + password)
    return new Promise((resolve, reject) => {
        resolve(true)
    })
}

export const register = async (username: string, password: string) => {
    console.log(username + " signed up with password " + password)
    return new Promise((resolve, reject) => {
        resolve(true)
    })
}

export const search = async (username: string): Promise<User[]> => {
    console.log("Search " + username)
    return new Promise((resolve, reject) => {
        resolve(users)
    })
}
