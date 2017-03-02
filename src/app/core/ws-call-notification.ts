export interface WsCallNotification {
    caller: {
        gps: {
            lat: number;
            lng: number;
        };
        svg?: {
            x: number;
            y: number;
        };
    };
    callee: {
        gps: {
            lat: number;
            lng: number;
        };
        svg?: {
            x: number;
            y: number;
        };
    };
}
