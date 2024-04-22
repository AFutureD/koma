import sqlite3
import subprocess
import struct
import click
import markdownify
import zlib
import binascii


def getNoteDetail(note_id: str) -> str :
    # completed_process = subprocess.run(
    #     ["osascript",
    #      "-e", 'tell application "Notes"',
    #      "-e", 'set theNote to note id "{}"'.format(note_id),
    #      '-e', 'return body of theNote',
    #      '-e', 'end tell'
    #      ],
    #     check = True,
    #     capture_output = True,
    #     encoding = "utf-8"
    # )
    # if completed_process.returncode != 0:
    #     raise Exception()
    # raw = completed_process.stdout
    # print(raw)

    raw = """
    <div>\n<h1><a id=\"note_2044\">Note 2044</a></h1>\n<div>\n<b>Account:</b> iCloud</div>\n<div>\n<b>Folder:</b> <span><a href=\"#folder_2\">Notes</a></span>\n</div>\n<div>\n<b>Title:</b> Title</div>\n<div>\n<b>Created:</b> 2024-03-24 09:43:11 +0000</div>\n<div>\n<b>Modified:</b> 2024-04-22 05:40:01 +0000</div>\n<div>\n<b>CloudKit Creator:</b> afuture.d@outlook.com</div>\n<div>\n<b>CloudKit Last Modified User:</b> afuture.d@outlook.com</div>\n<div>\n<b>CloudKit Last Modified Device:</b> Ninuo's MacBook Pro</div>\n<div class=\"note-content\">\n<h1>Title <br>\n</h1>\n<br><ul class=\"dashed\" data-apple-notes-indent-amount=\"0\">\n<li>df </li>\n<li>dsf </li>\n</ul>\n<br><ol data-apple-notes-indent-amount=\"0\">\n<li>史蒂夫sf</li>\n<li>第三方</li>\n</ol>\n<br><ul class=\"checklist\" data-apple-notes-indent-amount=\"0\">\n<li class=\"unchecked\">史蒂夫水电费s</li>\n<li class=\"checked\">史蒂夫</li>\n<li class=\"unchecked\">地方</li>\n</ul>\n<br><blockquote class=\"block-quote\" data-apple-notes-indent-amount=\"1\">第三方手动<br>第三方<br>\n</blockquote>\n<br><br><pre>code 阿斯顿爱上\n</pre>\n<br>嘻嘻第三方史蒂夫水电费<br><br><br>#test<br><br><a href=\"https://docs.python.org/zh-cn/3/library/typing.html\" target=\"_blank\">https://docs.python.org/zh-cn/3/library/typing.html</a><br><br><span><img src=\"../files/Accounts/0CF85441-0EBB-46A3-95AA-F82E349EAD2D/Previews/3E88F3F9-7D32-4EC1-919F-10F4034BFA16-1-200x200-0/1_96BACDEE-9AAF-4327-BE88-ADD1E320FA97/Preview.png\"><a href=\"https://docs.python.org/zh-cn/3/library/typing.html\">https://docs.python.org/zh-cn/3/library/typing.html</a></span><br><br><span><img src=\"../files/Accounts/0CF85441-0EBB-46A3-95AA-F82E349EAD2D/Previews/A755FBA4-925C-4555-A047-320DE9B76981-1-563x1000-0.png\"><a href=\"https://apps.apple.com/app/id1669903815\">https://apps.apple.com/app/id1669903815</a></span><br><a href=\"../files/Accounts/0CF85441-0EBB-46A3-95AA-F82E349EAD2D/Media/2D8F5C67-930D-498C-BD6F-217A98084008/1_15140E88-71D1-42C0-A360-EF4B1F7124E0/3FB10B1F-696B-4E8C-93AC-2465717B528F_1_102_o.jpeg\" class=\"attr\" data-apple-notes-zidentifier=\"994921EF-3025-4F84-8B56-E1D77C121BA0\"><img src=\"../files/Accounts/0CF85441-0EBB-46A3-95AA-F82E349EAD2D/Previews/994921EF-3025-4F84-8B56-E1D77C121BA0-1-89x192-0/1_1EC50859-0643-485E-8F8F-4446F59463B0/Preview.png\"></a><br><br><table>\n<tr>\n<td>dsf </td>\n<td>adf </td>\n</tr>\n<tr>\n<td>asd </td>\n<td>as </td>\n</tr>\n</table>\n<br><a href=\"../files/Accounts/0CF85441-0EBB-46A3-95AA-F82E349EAD2D/FallbackImages/84523CC3-A005-46B0-82E2-18BC927CC137/1_39A780E7-15EB-4455-8F92-A82A3C004D8E/FallbackImage.png\" class=\"attr\" data-apple-notes-zidentifier=\"84523CC3-A005-46B0-82E2-18BC927CC137\"><img src=\"../files/Accounts/0CF85441-0EBB-46A3-95AA-F82E349EAD2D/Previews/84523CC3-A005-46B0-82E2-18BC927CC137-1-768x768-0/2_A522D0E8-C173-46B4-8A65-DA29A8EA289F/Preview.png\"></a><br>\n</div>\n</div>
    """
    return markdownify.markdownify(raw)





def uvarint(data,pos):
    x = s = 0
    while True:
        b = data[pos]
        pos += 1
        x = x | ((b&0x7f)<<s)
        if b < 0x80: return x,pos
        s += 7

def readbytes(data,pos):
    l,pos = uvarint(data,pos)
    return data[pos:pos+l], pos+l

def readstruct(fmt,l):
    return lambda data,pos: (struct.unpack_from(fmt,data,pos)[0],pos+l)

readers = [ uvarint, readstruct('<d',8), readbytes, None, None, readstruct('<f',4) ]

# https://www.ciofecaforensics.com/2020/01/13/apple-notes-revisited-easy-embedded-objects/
# https://ciofecaforensics.com/2020/09/18/apple-notes-revisited-protobuf/

# https://github.com/threeplanetssoftware/apple_cloud_notes_parser
# https://github.com/dunhamsteve/notesutils/blob/master/notes2bear
def parse(data, schema):
    "parses a protobuf"
    obj = {}
    pos = 0
    while pos < len(data):
        val,pos = uvarint(data,pos)
        typ = val & 7
        key = val >> 3
        val, pos = readers[typ](data,pos)
        if key not in schema:
            continue
        name, repeated, typ = schema[key]
        if isinstance(typ, dict):
            val = parse(val, typ)
        if typ == 'string':
            val = val.decode('utf8')
        if repeated:
            val = obj.get(name,[]) + [val]
        obj[name] = val
    return obj



@click.command()
def cli():
    qry = """
    SELECT
        'x-coredata://' || zmd.z_uuid || '/ICNote/p' || note.z_pk AS id,
        note.ztitle1 AS title,
        folder.ztitle2 AS folder,
        datetime(note.zmodificationdate1 + 978307200, 'unixepoch') AS modifiedAt,
        note.zsnippet AS snippet,
        acc.zname AS account,
        note.zidentifier AS UUID,
        (note.zispasswordprotected = 1) as locked,
        (note.zispinned = 1) as pinned,
        (note.zhaschecklist = 1) as checklist,
        (note.zhaschecklistinprogress = 1) as checklistInProgress,
        bolb.ZDATA as content
    FROM 
        ziccloudsyncingobject AS note
    INNER JOIN ziccloudsyncingobject AS folder 
        ON note.zfolder = folder.z_pk
    LEFT JOIN ziccloudsyncingobject AS acc 
        ON note.zaccount4 = acc.z_pk
    LEFT JOIN z_metadata AS zmd ON 1=1
    LEFT JOIN ZICNOTEDATA AS bolb ON note.ZNOTEDATA = bolb.Z_PK
    WHERE
        note.ztitle1 IS NOT NULL AND
        note.zmodificationdate1 IS NOT NULL AND
        note.z_pk IS NOT NULL AND
        note.zmarkedfordeletion != 1 AND
        folder.zmarkedfordeletion != 1
    ORDER BY
        note.zmodificationdate1 DESC
    """

    con = sqlite3.connect("/Users/ninuo/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite")
    cur = con.cursor()
    res = cur.execute(qry)
    row = res.fetchall()

    print(getNoteDetail(""))

    # note_content = getNoteDetail("x-coredata://B9E6F60F-C970-4817-9C10-82195F366558/ICNote/p2044")
    # print(note_content)
