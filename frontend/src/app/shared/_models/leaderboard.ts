export interface LeaderboardApiData {
    daily: LeaderboardArray;
    weekly: LeaderboardArray;
    alltime: LeaderboardArray;
};

export type LeaderboardArray = {
    username: string;
    calls: number;
}[];
