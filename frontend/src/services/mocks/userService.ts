import { User } from "../../types"

let user: User = {
    "username": "bruna",
    "bio": "I am a software developer interested in animes and mangas.",
    "picture": "https://cdn-icons-png.flaticon.com/512/5968/5968350.png"
}

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
