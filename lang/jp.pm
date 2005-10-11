# language-specific definitions for ezmlm-web
# in Japanese

# The meanings of the various ezmlm-make command line switches. The default
# ones match the ezmlm-idx 0.4 default ezmlmrc ... Alter them to suit your
# own ezmlmrc. Removing options from this list makes them unavailable
# through ezmlm-web - this could be useful for things like -w

%EZMLM_LABELS = (
#   option => ['Short Name', 
#              'Long Help Description'],

      a => ['アーカイブ保存', 
            'メッセージをアーカイブする'],
      b => ['アーカイブブロック', 
            'モデレータのみアーカイブにアクセス可能'],
#     c => config. This is implicity called, so is not defined here
      d => ['ダイジェスト作成',
            'メッセージのダイジェストリストをセットアップする'], 
#     e => edit. Also implicity called, so not defined here
      f => ['件名にPrefixを付加する',
            '件名に指定したPrefix文字を付加する'],
      g => ['アーカイブ制限',
            '送信者が未登録の場合アーカイブのアクセスを拒否する'],
      h => ['登録確認をしない',
            'メールによる登録時に確認メールを送らない'],
      i => ['インデックス作成',
            'WWW アーカイブアクセス用インデックスの作成'],
      j => ['登録解除確認をしない',
            'メールによる登録解除時に確認メールを送らない'],
      k => ['拒否リスト有効',
            '拒否リストに登録されたアドレスを拒否する'], 
      l => ['登録者リスト取出',
            '遠隔管理者に登録者リストを送る'],
      m => ['投稿の審査',
            '全ての投稿メッセージを審査する'],
      n => ['テキスト編集', 
            '遠隔管理者にテキスト編集を許可する'],
      o => ['モデレータのみ投稿可', 
            'モデレータ以外の投稿を拒否する'],
      p => ['公開する',
            'メールによる登録、登録解除などを有効にする'],
      q => ['リクエスト形式有効',
            'local-request@host のメールを処理する'],
      r => ['遠隔管理',
            '遠隔管理を有効にする'],
      s => ['登録の審査',
            '登録を審査する'],
      t => ['Trailerを付加する',
            'メッセージの末尾にTrailerを付加する'], 
      u => ['登録者のみ投稿可',
            '登録者の投稿のみを受け付ける'], 
#     v => version. I doubt you will really need this ;-)
      w => ['警告を出さない',
            'ezmlm-warn(1) の挙動を抑止する'],
      x => ['指定mime typeの削除',
            '指定したmime typeの貼付ファイルを削除する'],
#     y => not used
#     z => not used

# These all take an extra argument, which is the default value to use

      0 => ['サブリストにする', 
            '指定したメインリストのサブリストにする',
            'mainlist@host'],   
#     1 => not used
#     2 => not used
      3 => ['送信者アドレス固定',
            '指定した Fromアドレスに固定する',
            'fromarg'],
      4 => ['ダイジェストオプション',
            'ezmlm-tstdig(1) のオプションを指定する',
            '-t24 -m30 -k64'],
      5 => ['オーナーアドレス',
            'リストオーナーのアドレスを指定する', 
            ''],
      6 => ['SQLデータベース',
            'SQLデータベースへの接続情報',
            'host:port:user:password:datab:table'],
      7 => ['メッセージモデレータのデータベース',
            'メッセージモデレータのデータベースへのフルパス',
            '/some/full/path'],
      8 => ['登録モデレータのデータベース',
            '登録モデレータのデータベースへのフルパス',
            '/some/full/path'],
      9 => ['遠隔管理者データベース',
            '遠隔管理者のデータベースへのフルパス',
            '/some/full/path']

);

# This list defines most of the context sensitive help in ezmlm-web. What
# isn't defined here is the options, which are defined above ... You can
# alter these if you feel something else would make more sense to your users
# Just be careful of what can fit on a screen!

%HELPER = (

   # These should be self explainitory
   addaddress       => 'RFC822 に準拠したメールアドレスを入れます 例; J Random User <jru@on.web.za>',
   addaddressfile   => 'または RFC822 に準拠したアドレスを、１行毎に含むテキストファイルを選択します',
   moderator        => 'モデレータ: 登録や投稿を審査する人のリスト',
   deny             => '拒絶リスト: メーリングリストへの参加を拒絶する人のリスト',
   allow            => '許可リスト: メーリングリストへの参加を特に許可する人のリスト',
   digest           => 'ダイジェストリスト: 全てのメッセージのダイジェストの受け取りを許可された人のリスト',
   webarch          => 'ウェブベースのアーカイブリストの閲覧',
   config           => 'メーリングリストの設定の変更',
   listname         => 'リスト選択時に表示される名前.また、実際に作成されるサブディレクトリの名前.',
   listadd          => 'メーリングリストの投稿に使用されるアドレス.特殊な場合を除き、- 以前は変更削除しないこと',
   webusers         => 'NB! 現在は、ここで指定できるユーザーは実在のユーザーに限る. ユーザーの追加は将来の追加課題',
   prefix           => '件名の先頭に付加される文字列 #で、メッセージ番号がつきます',
   headerremove     => 'メッセージから取り除くヘッダーを指定する',
   headeradd        => 'メッセージに追加するヘッダーを指定する',
   mimeremove       => '指定した mime type の貼付ファイルをメッセージから削除する',
   allowedit        => 'ユーザー名のカンマ区切りリストまたは、<CODE>ALL</CODE> (有効な全てのユーザー)',
   mysqlcreate      => 'MySQLに必要なテーブルを作成する'

);

# This defines the captions of each of the buttons in ezmlm-web, and allows 
# you to configure them for your own language or taste. Since these are used
# by the switching algorithm it is important that every button has a unique
# caption - ie we can't have two 'Edit' buttons doing different things.

%BUTTON = (
   
   # These MUST all be unique!
   create                => '作成',
   createlist            => 'リスト作成',
   edit                  => '編集',
   delete                => '削除',
   deleteaddress         => 'アドレス削除',
   addaddress            => 'アドレス追加',
   moderators            => 'モデレータ',
   denylist              => '拒絶リスト',
   allowlist             => '許可リスト',
   digestsubscribers     => 'ダイジェスト登録者',
   configuration         => '設定',
   yes                   => 'はい',
   no                    => 'いいえ',
   updateconfiguration   => '設定更新',
   edittexts             => 'テキスト編集',
   editfile              => 'ファイル編集',
   savefile              => 'ファイル保存',
   webarchive            => 'ウェブアーカイブ',
   selectlist            => 'リスト選択',
   subscribers           => '登録者編集',
   cancel                => 'キャンセル',
   resetform             => 'リセット',

);

# This defines the fixed text strings that are used in ezmlm-web. By editing
# these along with the button labels and help texts, you can convert ezmlm-web
# to another language :-) If anyone gets arround to doing complete templates
# for other languages I would appreciate a copy so that I can include it in
# future releases of ezmlm-web.

%LANGUAGE = (
   nop                   => 'Action not yet implemented',
   chooselistinfo        => "<UL><LI>メーリングリストを選択するか、または、 [$BUTTON{'create'}] ボタンを押して作成してください.<LI>変更する場合は、選択して、 [$BUTTON{'edit'}] ボタンを押してください.<LI>削除する場合は、選択して、 [$BUTTON{'delete'}] ボタンを押してください.</UL>",
   confirmdelete         => '削除確認', # list name
   subscribersto         => '登録者編集', # list name
   subscribers           => '登録者',
   additionalparts       => 'リスト付加情報',
   posting               => '投稿',
   subscription          => '登録',
   remoteadmin           => '遠隔管理',
   for                   => 'for', # as in; moderators for blahlist
   createnew             => '新規リスト作成',
   listname              => 'リスト名',
   listaddress           => 'リストアドレス',
   listoptions           => 'リストオプション',
   allowedtoedit         => 'リスト編集許可者',
   editconfiguration     => 'リスト設定編集',
   prefix                => '件名に付加する文字 prefix',
   headerremove          => '削除するヘッダー情報',
   headeradd             => '追加するヘッダー情報',
   mimeremove            => '削除する貼付ファイルのmime type',
   edittextinfo          => "左側にある一覧は、DIR/text の中にあるテキストファイルです. <BR>これらのファイルは、ユーザーのリクエストに対する返信内容,または、配信されるメールに付加される内容です.<P>このファイルを編集するには, 左の一覧から選択して、 [$BUTTON{'editfile'}] ボタンを押します.<P>終了または、中止するときは、[$BUTTON{'cancel'}] ボタンを押します.",
   editingfile           => 'ファイル編集',
   editfileinfo          => '<BIG><STRONG>マネージ用</STRONG></BIG><BR><TT><STRONG>&lt;#l#&gt;</STRONG></TT> リスト名<BR><TT><STRONG>&lt;#A#&gt;</STRONG></TT> 投稿者アドレス<BR><TT><STRONG>&lt;#R#&gt;</STRONG></TT> 投稿者が返信するアドレス<P><BIG><STRONG>メッセージ埋め込み用</STRONG></BIG><BR><TT><STRONG>&lt;#l#&gt;</STRONG></TT> リスト名<BR><TT><STRONG>&lt;#A#&gt;</STRONG></TT> 受け取りアドレス<BR><TT><STRONG>&lt;#R#&gt;</STRONG></TT> 拒絶アドレス</UL>',
   mysqlcreate           => '必要ならば MySQL データベースを作成',

);

#                      === Configuration file ends ===
