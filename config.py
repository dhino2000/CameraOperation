# 使用するPCごとに特定のパラメータを指定、保存先など

# PC名
# savedir_camera : baslerカメラの保存先
# movedst_camera : 保存した動画の移動先
# dir_database_network : databaseフォルダ(ネットワーク共有フォルダ)
# dir_database_drive : databaseフォルダ(Googleドライブ)
# path_gs : gs/binのパス
dict_config = {
    # 生理研,ハイスピードカメラ撮影用ワークステーション 1台目
    "HINTON": {
        "comport": {
            "camera_receiver": "COM5",
            "camera_sender": "COM7",
        },
        "savedir_camera": "D:/Videos",
        "movedst_camera": "X:/database",
        "dir_database_network": "X:/database",
        "dir_database_drive": "G:/マイドライブ/database",
        "path_gs": "C:/Program Files/gs/gs10.01.1/bin",
    },
    # 生理研,ハイスピードカメラ撮影用ワークステーション 2台目
    "r558-d01": {
        "comport": {
            "camera_receiver": "COM5",
            "camera_sender": "COM7",
        },
        "savedir_camera": "D:/Videos",
        "movedst_camera": "Z:/database",
        "dir_database_network": "Z:/database",
        "dir_database_drive": "G:/マイドライブ/database",
        "path_gs": "C:/Program Files/gs/gs10.01.1/bin",
    },
    # 生理研,解析用ワークステーション
    "UltraPC_Smee": {
        "comport": {
            "camera_receiver": "",
            "camera_sender": "",
        },
        "savedir_camera": "C:/Users/tanis/Videos",
        "movedst_camera": "Z:/database",
        "dir_database_network": "Z:/database",
        "dir_database_drive": "G:/マイドライブ/database",
        "path_gs": "C:/Program Files/gs/gs10.01.1/bin",
    },
    # 名大,ハイスピードカメラ撮影用ノートPC
    "DESKTOP-LH7UTSI": {
        "comport": {
            "camera_receiver": "COM12",
            "camera_sender": "COM13",
        },
        "savedir_camera": "C:/Users/fukat/Videos",
        "movedst_camera": "Z:/Mio Inoue NAS3/database",
        "dir_database_network": "Z:/database",
        "dir_database_drive": "G:/マイドライブ/database",
        "path_gs": "C:/Program Files/gs/gs10.01.1/bin",
    },
    # 名大,ハイスピードカメラ撮影用ノートPC 2台目
    "Behabior_NU_23": {
        "comport": {
            "camera_receiver": "COM8",
            "camera_sender": "COM9",
        },
        "savedir_camera": "C:/Users/behav/Videos",
        "movedst_camera": "Z:/Mio Inoue NAS3/database",
        "dir_database_network": "Z:/database",
        "dir_database_drive": "G:/マイドライブ/database",
        "path_gs": "C:/Program Files/gs/gs10.01.1/bin",
    },

    # 髙橋さんPC
    "Tkhs-7": {
        "comport": {
            "camera_receiver": "COM5",
            "camera_sender": "COM7",
        },
        "savedir_camera": "C:/Users/share/Videos",
        "movedst_camera": "Z:/database",
        "dir_database_network": "Z:/database",
        "dir_database_drive": "G:/マイドライブ/database",
        "path_gs": "C:/Program Files/gs/gs10.01.1/bin",
    },
    # 2階共用PC
    "DESKTOP-0TVK6UL": {
        "comport": {
            "camera_receiver": "COM5",
            "camera_sender": "COM7",
        },
        "savedir_camera": "C:/Users/share/Videos",
        "movedst_camera": "Z:/database",
        "dir_database_network": "Z:/database",
        "dir_database_drive": "G:/マイドライブ/database",
        "path_gs": "C:/Program Files/gs/gs10.01.1/bin",
    },
    # 生理研竹田PC
    "DESKTOP-5993JEL": {
        "comport": {
            "camera_receiver": "COM5",
            "camera_sender": "COM7",
        },
        "savedir_camera": "C:/Users/share/Videos",
        "movedst_camera": "Z:/database",
        "dir_database_network": "Z:/database",
        "dir_database_drive": "G:/マイドライブ/database",
        "path_gs": "C:/Program Files/gs/gs10.01.1/bin",
    },
    # 名大PC9
    "wakelabPC_2023": {
        "comport": {
            "camera_receiver": "COM5",
            "camera_sender": "COM7",
        },
        "savedir_camera": "C:/Users/share/Videos",
        "movedst_camera": "Z:/database",
        "dir_database_network": "Z:/database",
        "dir_database_drive": "G:/マイドライブ/database",
        "path_gs": "C:/Program Files/gs/gs10.01.1/bin",
    },
    # 名大PC10
    "wakelab": {
        "comport": {
            "camera_receiver": "COM5",
            "camera_sender": "COM7",
        },
        "savedir_camera": "C:/Users/share/Videos",
        "movedst_camera": "Z:/database",
        "dir_database_network": "G:/My Drive/database",
        "dir_database_drive": "G:/My Drive/database",
        "path_gs": "C:/Program Files/gs/gs10.01.1/bin",
    },
    # 名大PC10
    "wakelabPC10": {
        "comport": {
            "camera_receiver": "COM5",
            "camera_sender": "COM7",
        },
        "savedir_camera": "C:/Users/share/Videos",
        "movedst_camera": "Z:/database",
        "dir_database_network": "G:/My Drive/database",
        "dir_database_drive": "G:/My Drive/database",
        "path_gs": "C:/Program Files/gs/gs10.01.1/bin",
    },    
    # 深津ノートパソコン
    "DESKTOP-507ML75": {
        "comport": {
            "camera_receiver": "COM5",
            "camera_sender": "COM7",
        },
        "savedir_camera": "C:/Users/share/Videos",
        "movedst_camera": "Z:/database",
        "dir_database_network": "Z:/database",
        "dir_database_drive": "H:/マイドライブ/database",
        "path_gs": "C:/Program Files/gs/gs10.01.1/bin",
    },
}