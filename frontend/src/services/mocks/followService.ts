import { User } from "../../types"

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

export const fetchRecommendation = async (username: string): Promise<User[]> => {
    return new Promise((resolve, reject) => {
        resolve(users)
    })
}

export const follow = async (username: string, followed:string) => {
    console.log(username + " followed " + followed)
}
