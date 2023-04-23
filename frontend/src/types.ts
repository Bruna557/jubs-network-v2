export type Post = {
    username: string,
    posted_on: string,
    body: string,
    likes: number,
    picture: string
}

export type User = {
    username: string,
    bio: string,
    picture: string
    is_followed?: boolean
}

export type TimelineResult = {
    posts: Post[],
    has_more: boolean
}

export type UsersResult = {
    result: User[]
    has_more: boolean
}
