export interface BasicInformationApiData {
  alltimeCalls: number;
  dailyCalls: number;
  weeklyCalls: number;
  dailyLeaderboard: LeaderboardArray;
};

type LeaderboardArray = {
  username: string;
  calls: number;
}[];
