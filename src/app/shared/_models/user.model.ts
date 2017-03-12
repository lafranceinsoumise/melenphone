export class User {
  id: number;
  agentUsername: string;
  email: string;
  location: {
      city: string;
      country_code: string;
  };
  phi: number;
  phi_multiplier: number;
  alltime_leaderboard: number;
  weekly_leaderboard: number;
  daily_leaderboard: number;
}
