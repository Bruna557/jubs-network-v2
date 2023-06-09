import { User, UsersResult } from "../../types"

let user: User = {
    "username": "bruna",
    "bio": "I am a software developer interested in programming and software architecture.",
    "picture": "https://cdn-icons-png.flaticon.com/512/5968/5968350.png"
}

let users = [
    {

        "username": "lilith",
        "bio": "I am a cat interested in shoelaces and garbage.",
        "picture": "https://cdn-icons-png.flaticon.com/512/2373/2373010.png",
        "is_followed": true
    },
    {

        "username": "jubs",
        "bio": "I am a dog interested in toys, bones and walks.",
        "picture": "https://cdn-icons-png.flaticon.com/512/8876/8876508.png",
        "is_followed": false
    },
    {

        "username": "ryuk",
        "bio": "I am a god of death interested in apples.",
        "picture": "https://cdn-icons-png.flaticon.com/512/415/415682.png",
        "is_followed": true
    }
]

export const fetchUser = async (username: string): Promise<User> => {
    return new Promise((resolve, reject) => {
        resolve(user)
    })
}

export const changeBio = async (username: string, bio: string) => {
    console.log("Changed bio " + bio)
    return {"bio": bio}
}

export const changePicture = async (username: string, picture: string) => {
    console.log("Changed picture " + picture)
    return {"picture": picture}
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

export const register = async (username: string, password: string, bio: string, picture: string) => {
    console.log(username + " signed up with password " + password)
    return new Promise((resolve, reject) => {
        resolve(true)
    })
}

export const search = async (username: string, q: string, page_number: number): Promise<UsersResult> => {
    console.log("Search " + q)
    return new Promise((resolve, reject) => {
        resolve({has_more: false, result: users})
    })
}

export const fetchRecommendation = async (username: string): Promise<UsersResult> => {
    return new Promise((resolve, reject) => {
        resolve({has_more: false, result: users})
    })
}

export const follow = async (username: string, followed: string) => {
    console.log(username + " followed " + followed)
}

export const unfollow = async (username: string, followed: string) => {
    console.log(username + " unfollowed " + followed)
}

export const fetchFollowers = async (username: string, page_number: number): Promise<UsersResult> => {
    return new Promise((resolve, reject) => {
        resolve({has_more: false, result: users})
    })
}

export const fetchFollowing = async (username: string, page_number: number): Promise<UsersResult> => {
    return new Promise((resolve, reject) => {
        resolve({has_more: false, result: users})
    })
}
