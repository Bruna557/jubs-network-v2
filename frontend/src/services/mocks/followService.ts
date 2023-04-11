import { User } from "../../types"

let users: User[] = [
    {
        "username": "bruna",
        "bio": "I am a software develop interested in animes and mangas.",
        "picture": "https://cdn-icons-png.flaticon.com/512/99/99428.png"
    },
    {
        "username": "jubs",
        "bio": "I am a dog interested in toys, bones and walks.",
        "picture": "https://cdn-icons-png.flaticon.com/512/4540/4540592.png"
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
