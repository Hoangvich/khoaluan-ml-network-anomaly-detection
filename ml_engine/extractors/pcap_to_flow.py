import os
import sys
import time
import socket
import dpkt
import numpy as np
import pandas as pd

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

FEATURE_COLS = [
    'ACK Flag Count', 'Active Max', 'Active Mean', 'Active Min', 'Active Std',
    'Average Packet Size', 'Bwd Header Length', 'Bwd IAT Max', 'Bwd IAT Mean',
    'Bwd IAT Min', 'Bwd IAT Std', 'Bwd IAT Total', 'Bwd Packet Length Max',
    'Bwd Packet Length Mean', 'Bwd Packet Length Min', 'Bwd Packet Length Std',
    'Bwd Packets/s', 'Down/Up Ratio', 'ECE Flag Count', 'FIN Flag Count',
    'Flow Bytes/s', 'Flow Duration', 'Flow IAT Max', 'Flow IAT Mean',
    'Flow IAT Min', 'Flow IAT Std', 'Flow Packets/s', 'Fwd Header Length',
    'Fwd IAT Max', 'Fwd IAT Mean', 'Fwd IAT Min', 'Fwd IAT Std',
    'Fwd IAT Total', 'Fwd PSH Flags', 'Fwd Packet Length Max',
    'Fwd Packet Length Mean', 'Fwd Packet Length Min', 'Fwd Packet Length Std',
    'Fwd Packets/s', 'Fwd URG Flags', 'Idle Max', 'Idle Mean', 'Idle Min',
    'Idle Std', 'Init_Win_bytes_backward', 'Init_Win_bytes_forward',
    'Max Packet Length', 'Min Packet Length', 'PSH Flag Count',
    'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance',
    'RST Flag Count', 'SYN Flag Count', 'Total Backward Packets',
    'Total Fwd Packets', 'Total Length of Bwd Packets',
    'Total Length of Fwd Packets', 'URG Flag Count', 'act_data_pkt_fwd',
    'min_seg_size_forward', 'dst_port_class'
]

def inet_to_str(inet):
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except Exception:
        try:
            return socket.inet_ntop(socket.AF_INET6, inet)
        except Exception:
            return "0.0.0.0"

class FlowRecord:
    def __init__(self, src_ip, sport, dst_ip, dport, proto, start_ts):
        self.src_ip = src_ip
        self.sport = sport
        self.dst_ip = dst_ip
        self.dport = dport
        self.proto = proto
        self.start_ts = start_ts
        self.last_ts = start_ts
        
        # Danh sách gói tin
        self.fwd_ts = []
        self.bwd_ts = []
        self.all_ts = []
        
        self.fwd_lens = []
        self.bwd_lens = []
        self.all_lens = []
        
        self.fwd_hdr_lens = []
        self.bwd_hdr_lens = []
        
        # Flags
        self.fin_cnt = 0
        self.syn_cnt = 0
        self.rst_cnt = 0
        self.psh_cnt = 0
        self.ack_cnt = 0
        self.urg_cnt = 0
        self.ece_cnt = 0
        self.fwd_psh = 0
        self.fwd_urg = 0
        
        # Window & Seg size
        self.init_win_fwd = -1
        self.init_win_bwd = -1
        self.act_data_pkt_fwd = 0
        self.fwd_seg_sizes = []

    def add_packet(self, ts, pkt_len, hdr_len, is_fwd, flags=0, win=-1, payload_len=0, seg_size=0):
        self.last_ts = ts
        self.all_ts.append(ts)
        self.all_lens.append(pkt_len)
        
        # Flags
        if flags:
            fin = bool(flags & dpkt.tcp.TH_FIN)
            syn = bool(flags & dpkt.tcp.TH_SYN)
            rst = bool(flags & dpkt.tcp.TH_RST)
            psh = bool(flags & dpkt.tcp.TH_PUSH)
            ack = bool(flags & dpkt.tcp.TH_ACK)
            urg = bool(flags & dpkt.tcp.TH_URG)
            ece = bool(flags & dpkt.tcp.TH_ECE)
            
            self.fin_cnt += fin
            self.syn_cnt += syn
            self.rst_cnt += rst
            self.psh_cnt += psh
            self.ack_cnt += ack
            self.urg_cnt += urg
            self.ece_cnt += ece

        if is_fwd:
            self.fwd_ts.append(ts)
            self.fwd_lens.append(pkt_len)
            self.fwd_hdr_lens.append(hdr_len)
            if self.init_win_fwd == -1 and win != -1:
                self.init_win_fwd = win
            if payload_len > 0:
                self.act_data_pkt_fwd += 1
            if seg_size > 0:
                self.fwd_seg_sizes.append(seg_size)
            if flags:
                self.fwd_psh += bool(flags & dpkt.tcp.TH_PUSH)
                self.fwd_urg += bool(flags & dpkt.tcp.TH_URG)
        else:
            self.bwd_ts.append(ts)
            self.bwd_lens.append(pkt_len)
            self.bwd_hdr_lens.append(hdr_len)
            if self.init_win_bwd == -1 and win != -1:
                self.init_win_bwd = win

    def compute_features(self):
        duration_sec = max(1e-6, self.last_ts - self.start_ts)
        duration_us = duration_sec * 1e6
        
        tot_fwd = len(self.fwd_lens)
        tot_bwd = len(self.bwd_lens)
        tot_all = tot_fwd + tot_bwd
        
        tot_fwd_len = float(sum(self.fwd_lens))
        tot_bwd_len = float(sum(self.bwd_lens))
        
        fwd_lens_arr = np.array(self.fwd_lens, dtype=np.float32) if tot_fwd else np.array([0.0], dtype=np.float32)
        bwd_lens_arr = np.array(self.bwd_lens, dtype=np.float32) if tot_bwd else np.array([0.0], dtype=np.float32)
        all_lens_arr = np.array(self.all_lens, dtype=np.float32) if tot_all else np.array([0.0], dtype=np.float32)
        
        # Inter-arrival times (IATs) in microseconds
        def get_iat_stats(ts_list):
            if len(ts_list) <= 1:
                return 0.0, 0.0, 0.0, 0.0, 0.0
            arr = np.diff(ts_list) * 1e6
            return float(np.sum(arr)), float(np.mean(arr)), float(np.std(arr)), float(np.max(arr)), float(np.min(arr))
            
        f_tot, f_mean, f_std, f_max, f_min = get_iat_stats(self.fwd_ts)
        b_tot, b_mean, b_std, b_max, b_min = get_iat_stats(self.bwd_ts)
        _, all_mean, all_std, all_max, all_min = get_iat_stats(self.all_ts)
        
        # Active and Idle stats (Idle threshold = 1.0 second = 1,000,000 us)
        idles, actives = [], []
        if len(self.all_ts) > 1:
            diffs = np.diff(self.all_ts) * 1e6
            cur_active = 0.0
            for d in diffs:
                if d >= 1000000.0:
                    idles.append(d)
                    if cur_active > 0:
                        actives.append(cur_active)
                        cur_active = 0.0
                else:
                    cur_active += d
            if cur_active > 0:
                actives.append(cur_active)
                
        def get_summary(arr):
            if not arr:
                return 0.0, 0.0, 0.0, 0.0
            return float(np.mean(arr)), float(np.std(arr)), float(np.max(arr)), float(np.min(arr))
            
        act_mean, act_std, act_max, act_min = get_summary(actives)
        idle_mean, idle_std, idle_max, idle_min = get_summary(idles)
        
        # dst_port_class: 0: 0-1023, 1: 1024-49151, 2: 49152+
        if self.dport < 1024:
            port_class = 0
        elif self.dport < 49152:
            port_class = 1
        else:
            port_class = 2

        min_seg = float(min(self.fwd_seg_sizes)) if self.fwd_seg_sizes else 0.0
        down_up = float(tot_bwd / tot_fwd) if tot_fwd > 0 else 0.0
        avg_pkt_size = float(np.mean(all_lens_arr)) if tot_all else 0.0

        row = {
            'ACK Flag Count': float(self.ack_cnt),
            'Active Max': act_max,
            'Active Mean': act_mean,
            'Active Min': act_min,
            'Active Std': act_std,
            'Average Packet Size': avg_pkt_size,
            'Bwd Header Length': float(sum(self.bwd_hdr_lens)),
            'Bwd IAT Max': b_max,
            'Bwd IAT Mean': b_mean,
            'Bwd IAT Min': b_min,
            'Bwd IAT Std': b_std,
            'Bwd IAT Total': b_tot,
            'Bwd Packet Length Max': float(np.max(bwd_lens_arr)),
            'Bwd Packet Length Mean': float(np.mean(bwd_lens_arr)),
            'Bwd Packet Length Min': float(np.min(bwd_lens_arr)),
            'Bwd Packet Length Std': float(np.std(bwd_lens_arr)),
            'Bwd Packets/s': float(tot_bwd / duration_sec),
            'Down/Up Ratio': down_up,
            'ECE Flag Count': float(self.ece_cnt),
            'FIN Flag Count': float(self.fin_cnt),
            'Flow Bytes/s': float((tot_fwd_len + tot_bwd_len) / duration_sec),
            'Flow Duration': duration_us,
            'Flow IAT Max': all_max,
            'Flow IAT Mean': all_mean,
            'Flow IAT Min': all_min,
            'Flow IAT Std': all_std,
            'Flow Packets/s': float(tot_all / duration_sec),
            'Fwd Header Length': float(sum(self.fwd_hdr_lens)),
            'Fwd IAT Max': f_max,
            'Fwd IAT Mean': f_mean,
            'Fwd IAT Min': f_min,
            'Fwd IAT Std': f_std,
            'Fwd IAT Total': f_tot,
            'Fwd PSH Flags': float(self.fwd_psh),
            'Fwd Packet Length Max': float(np.max(fwd_lens_arr)),
            'Fwd Packet Length Mean': float(np.mean(fwd_lens_arr)),
            'Fwd Packet Length Min': float(np.min(fwd_lens_arr)),
            'Fwd Packet Length Std': float(np.std(fwd_lens_arr)),
            'Fwd Packets/s': float(tot_fwd / duration_sec),
            'Fwd URG Flags': float(self.fwd_urg),
            'Idle Max': idle_max,
            'Idle Mean': idle_mean,
            'Idle Min': idle_min,
            'Idle Std': idle_std,
            'Init_Win_bytes_backward': float(self.init_win_bwd),
            'Init_Win_bytes_forward': float(self.init_win_fwd),
            'Max Packet Length': float(np.max(all_lens_arr)),
            'Min Packet Length': float(np.min(all_lens_arr)),
            'PSH Flag Count': float(self.psh_cnt),
            'Packet Length Mean': float(np.mean(all_lens_arr)),
            'Packet Length Std': float(np.std(all_lens_arr)),
            'Packet Length Variance': float(np.var(all_lens_arr)),
            'RST Flag Count': float(self.rst_cnt),
            'SYN Flag Count': float(self.syn_cnt),
            'Total Backward Packets': float(tot_bwd),
            'Total Fwd Packets': float(tot_fwd),
            'Total Length of Bwd Packets': tot_bwd_len,
            'Total Length of Fwd Packets': tot_fwd_len,
            'URG Flag Count': float(self.urg_cnt),
            'act_data_pkt_fwd': float(self.act_data_pkt_fwd),
            'min_seg_size_forward': min_seg,
            'dst_port_class': int(port_class)
        }
        return row

def extract_flows_from_pcap(pcap_path, label, flow_timeout=120.0):
    """
    Doc pcap sieu toc bang dpkt, nhom luong 5-tuple va tinh toan 62 dac trung.
    """
    print(f"\n-> Đang xử lý: {os.path.basename(pcap_path)} (Gán nhãn: {label})...")
    t0 = time.time()
    flows = {}
    completed_flows = []
    pkt_count = 0
    
    with open(pcap_path, 'rb') as fp:
        pcap_reader = dpkt.pcap.Reader(fp)
        for ts, buf in pcap_reader:
            pkt_count += 1
            try:
                eth = dpkt.ethernet.Ethernet(buf)
                if not isinstance(eth.data, (dpkt.ip.IP, dpkt.ip6.IP6)):
                    continue
                ip = eth.data
                src_ip = inet_to_str(ip.src)
                dst_ip = inet_to_str(ip.dst)
                proto = ip.p
                
                pkt_len = len(buf)
                ip_hdr_len = ip.hl * 4 if hasattr(ip, 'hl') else 40
                
                if isinstance(ip.data, dpkt.tcp.TCP):
                    tcp = ip.data
                    sport, dport = tcp.sport, tcp.dport
                    tcp_hdr_len = tcp.off * 4
                    total_hdr_len = ip_hdr_len + tcp_hdr_len
                    flags = tcp.flags
                    win = tcp.win
                    payload_len = len(tcp.data)
                    seg_size = tcp_hdr_len
                elif isinstance(ip.data, dpkt.udp.UDP):
                    udp = ip.data
                    sport, dport = udp.sport, udp.dport
                    total_hdr_len = ip_hdr_len + 8
                    flags = 0
                    win = -1
                    payload_len = len(udp.data)
                    seg_size = 8
                else:
                    continue
                    
                fwd_key = (src_ip, sport, dst_ip, dport, proto)
                bwd_key = (dst_ip, dport, src_ip, sport, proto)
                
                if fwd_key in flows:
                    f = flows[fwd_key]
                    if (ts - f.last_ts) > flow_timeout:
                        completed_flows.append(f.compute_features())
                        flows[fwd_key] = FlowRecord(src_ip, sport, dst_ip, dport, proto, ts)
                        f = flows[fwd_key]
                    f.add_packet(ts, pkt_len, total_hdr_len, is_fwd=True, flags=flags, win=win, payload_len=payload_len, seg_size=seg_size)
                elif bwd_key in flows:
                    f = flows[bwd_key]
                    if (ts - f.last_ts) > flow_timeout:
                        completed_flows.append(f.compute_features())
                        flows[bwd_key] = FlowRecord(dst_ip, dport, src_ip, sport, proto, ts)
                        f = flows[bwd_key]
                    f.add_packet(ts, pkt_len, total_hdr_len, is_fwd=False, flags=flags, win=win, payload_len=payload_len, seg_size=seg_size)
                else:
                    f = FlowRecord(src_ip, sport, dst_ip, dport, proto, ts)
                    f.add_packet(ts, pkt_len, total_hdr_len, is_fwd=True, flags=flags, win=win, payload_len=payload_len, seg_size=seg_size)
                    flows[fwd_key] = f
                    
            except Exception:
                continue

    # Flush cac luong con lai
    for f in flows.values():
        completed_flows.append(f.compute_features())
        
    dur = time.time() - t0
    print(f"   Hoàn thành {pkt_count:,} gói tin trong {dur:.2f}s -> Tạo ra {len(completed_flows):,} luồng mạng!")
    
    df = pd.DataFrame(completed_flows)
    if not df.empty:
        df['label'] = label
        df['source_dataset'] = 'Lab'
        df['source_file'] = os.path.basename(pcap_path)
    return df

def convert_all_lab_pcaps():
    print("=" * 70)
    print("🔥 BẮT ĐẦU CONVERT TOÀN BỘ 4 FILE PCAP PHÒNG LAB THÀNH DỮ LIỆU FLOW")
    print("=" * 70)
    
    pcap_dir = "file pcap/file pcap"
    configs = [
        ("benign.pcap", "BENIGN"),
        ("ddos.pcap", "DoS/DDoS"),
        ("portscan.pcap", "PortScan"),
        ("bruteforce.pcap", "BruteForce"),
    ]
    
    dfs = []
    total_start = time.time()
    
    for filename, label in configs:
        path = os.path.join(pcap_dir, filename)
        if os.path.exists(path):
            df_part = extract_flows_from_pcap(path, label)
            dfs.append(df_part)
        else:
            print(f"⚠️ Cảnh báo: Không tìm thấy {path}")
            
    if not dfs:
        print("❌ Không có dữ liệu để chuyển đổi!")
        return None
        
    df_all = pd.concat(dfs, ignore_index=True)
    
    # Ép kiểu float32 cho tất cả đặc trưng số để chuẩn hóa
    for col in FEATURE_COLS:
        if col == 'dst_port_class':
            df_all[col] = df_all[col].astype(np.int8)
        else:
            df_all[col] = df_all[col].astype(np.float32)
            
    # Tạo group_id cho Lab traffic để chia fold nếu cần
    df_all['group_id'] = 'lab_' + df_all['label'] + '_' + df_all.index.astype(str)
    df_all['attack_subtype'] = df_all['label']
    
    # Sắp xếp đúng thứ tự cột như unified.parquet
    desired_cols = FEATURE_COLS + ['label', 'attack_subtype', 'source_dataset', 'source_file', 'group_id']
    df_all = df_all[desired_cols]
    
    out_dir = "data/processed"
    os.makedirs(out_dir, exist_ok=True)
    out_parquet = os.path.join(out_dir, "lab_traffic_cleaned.parquet")
    df_all.to_parquet(out_parquet, index=False)
    
    total_time = time.time() - total_start
    print("\n" + "=" * 70)
    print("🎉 CONVERT THÀNH CÔNG TOÀN BỘ DỮ LIỆU LAB!")
    print(f"- Tổng thời gian xử lý: {total_time:.2f} giây")
    print(f"- Tổng số luồng trích xuất: {len(df_all):,} luồng")
    print("- Phân bố nhãn trích xuất từ Lab:")
    print(df_all['label'].value_counts().to_string())
    print(f"\n[OK] Đã lưu file Parquet chuẩn tại: {out_parquet}")
    print("=" * 70)
    
    return df_all

if __name__ == "__main__":
    convert_all_lab_pcaps()
