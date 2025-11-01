export function timeNumberToString(value: number) {
    const hours = Math.floor(value / 2);
    const minutes = (value % 2) * 30;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
}