# audit/ (append-only)

- quarantine_queue.jsonl: nơi ghi các entity bị cách ly (gate fail / fraud / bad evidence)
- kill_switch_log.jsonl: nhật ký kích hoạt cầu dao (manual/systems)

Nguyên tắc:
- Không sửa dòng cũ. Muốn cập nhật trạng thái, append record mới.
