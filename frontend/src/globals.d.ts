export {}

declare global {
    var aq: any;

    interface Column {
        key: string;
        label: string;
        width?: number;
    }
    
    interface Row {
        [key: string]: string | number;
    }

    interface Month {
        name: string;
        abb: string;
    }
}