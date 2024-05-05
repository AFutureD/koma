-- list all notes
SELECT
    note.z_pk as z_pk,
    note.zidentifier AS uuid,
    'x-coredata://' || zmd.z_uuid || '/ICNote/p' || note.z_pk AS url_scheme,
    note.ztitle1 AS title,
    folder.ztitle2 AS folder,
    datetime(note.zmodificationdate1 + 978307200, 'unixepoch') AS modified_at,
    note.ZWIDGETSNIPPET AS preview,
    COALESCE(note.ZACCOUNT, note.ZACCOUNT1, note.ZACCOUNT2, note.ZACCOUNT3, note.ZACCOUNT4,
             note.ZACCOUNT5, note.ZACCOUNT6, note.ZACCOUNT7, note.ZACCOUNT8) AS account,
    (note.zispasswordprotected = 1) as locked,
    (note.zispinned = 1) as pinned,
    bolb.ZDATA as content
FROM
    ziccloudsyncingobject AS note
INNER JOIN ziccloudsyncingobject AS folder
    ON note.zfolder = folder.z_pk
LEFT JOIN z_metadata AS zmd ON 1=1
LEFT JOIN ZICNOTEDATA AS bolb ON note.ZNOTEDATA = bolb.Z_PK
WHERE
    note.ztitle1 IS NOT NULL AND
    note.zmodificationdate1 IS NOT NULL AND
    note.z_pk IS NOT NULL AND
    note.zmarkedfordeletion != 1 AND
    folder.zmarkedfordeletion != 1 AND
    note.zispasswordprotected = 0
ORDER BY
    note.zmodificationdate1 DESC
;

-- list all account
SELECT Z_PK, ZNAME, ZIDENTIFIER FROM ZICCLOUDSYNCINGOBJECT WHERE ZUSERRECORDNAME IS NOT NULL;



-- list all attachments
SELECT ZIDENTIFIER as attachement_uuid, COALESCE(ZTYPEUTI, ZTYPEUTI1) as uti from ZICCLOUDSYNCINGOBJECT
WHERE
    ZTYPEUTI is not  null or ZTYPEUTI1 is not null
;

 -- unified query for all attachments
SELECT
    attachment.Z_PK as z_pk,
    attachment.ZIDENTIFIER as attachment_identifier,
    COALESCE(attachment.ZTYPEUTI, attachment.ZTYPEUTI1) as attachment_uti,
    COALESCE(attachment.ZNOTE, attachment.ZNOTE1) as note_pk,
    COALESCE(attachment.ZACCOUNT, attachment.ZACCOUNT1, attachment.ZACCOUNT2, attachment.ZACCOUNT3, attachment.ZACCOUNT4,
            attachment.ZACCOUNT5, attachment.ZACCOUNT6, attachment.ZACCOUNT7, attachment.ZACCOUNT8) AS account,
    CASE
        -- url
        WHEN attachment.ZTYPEUTI = 'public.url' THEN attachment.ZTITLE
        -- tag
        WHEN attachment.ZTYPEUTI1 = 'com.apple.notes.inlinetextattachment.hashtag' THEN attachment.ZALTTEXT
        -- table
        WHEN attachment.ZTYPEUTI = 'com.apple.notes.table' THEN attachment.ZSUMMARY
        -- draw
        WHEN attachment.ZTYPEUTI = 'com.apple.paper' THEN attachment.ZSUMMARY
        WHEN attachment.ZTYPEUTI = 'com.apple.drawing.2' THEN attachment.ZSUMMARY
        WHEN attachment.ZTYPEUTI = 'com.apple.drawing' THEN attachment.ZSUMMARY
        -- gallery
        WHEN attachment.ZTYPEUTI = 'com.apple.notes.gallery' THEN attachment.ZTITLE
        -- media
        WHEN attachment.ZMEDIA is not null THEN attachment.ZOCRSUMMARY -- ZOCRSUMMARY + ZIMAGECLASSIFICATIONSUMMARY
        ELSE null
    END as attachment_text,
    COALESCE(attachment.ZPARENTATTACHMENT, attachment.ZPARENTATTACHMENT1) as parent_pk,
    -- attachment.ZISPASSWORDPROTECTED as locked
    -- generation used for media and drawing
    COALESCE(attachment.ZFALLBACKIMAGEGENERATION, blob.ZGENERATION, blob.ZGENERATION1) as generation,

    -- url public.url
    attachment.ZURLSTRING as url,
    -- list all tables com.apple.notes.table or com.apple.notes.gallery
    attachment.ZMERGEABLEDATA1 as blob_data,
    -- list all drawing 'com.apple.paper' 'com.apple.drawing.2' 'com.apple.drawing'
    attachment.ZHANDWRITINGSUMMARY as draw_summary,
    -- MEDIA attachment.ZMEDIA as media_pk,
    blob.ZIDENTIFIER as file_uuid,
    blob.ZFILENAME as file_name
from ZICCLOUDSYNCINGOBJECT as attachment
LEFT JOIN ZICCLOUDSYNCINGOBJECT as blob
    on  attachment.ZMEDIA = blob.Z_PK and blob.ZATTACHMENT1 = attachment.Z_PK
WHERE
    (attachment.ZTYPEUTI is not null or attachment.ZTYPEUTI1 is not null)
    and attachment.ZISPASSWORDPROTECTED = 0
;

--  using case statement
SELECT
    attachment.ZIDENTIFIER as attachment_uuid,
    COALESCE(attachment.ZTYPEUTI, attachment.ZTYPEUTI1) as uti,
    attachment.ZNOTE as note_pk,
    CASE
        -- url
        WHEN attachment.ZTYPEUTI = 'public.url' THEN attachment.ZTITLE
        -- tag
        WHEN attachment.ZTYPEUTI1 = 'com.apple.notes.inlinetextattachment.hashtag' THEN attachment.ZALTTEXT
        -- table
        WHEN attachment.ZTYPEUTI = 'com.apple.notes.table' THEN attachment.ZSUMMARY
        -- draw
        WHEN attachment.ZTYPEUTI = 'com.apple.paper' THEN attachment.ZSUMMARY
        WHEN attachment.ZTYPEUTI = 'com.apple.drawing.2' THEN attachment.ZSUMMARY
        WHEN attachment.ZTYPEUTI = 'com.apple.drawing' THEN attachment.ZSUMMARY
        -- media
        WHEN attachment.ZMEDIA is not null THEN attachment.ZOCRSUMMARY -- ZOCRSUMMARY + ZIMAGECLASSIFICATIONSUMMARY
        ELSE null
    END as attachment_text,
    COALESCE(attachment.ZFALLBACKIMAGEGENERATION, blob.ZGENERATION, blob.ZGENERATION1) as generation,

    -- url public.url
    attachment.ZURLSTRING as url,
    -- list all tables com.apple.notes.table
    attachment.ZMERGEABLEDATA1 as bolb_data,
    -- list all drawing 'com.apple.paper' 'com.apple.drawing.2' 'com.apple.drawing'
    attachment.ZHANDWRITINGSUMMARY as draw_summary,
    -- MEDIA attachment.ZMEDIA as media_pk,
    blob.ZIDENTIFIER as file_uuid,
    blob.ZFILENAME as file_name
from ZICCLOUDSYNCINGOBJECT as attachment
LEFT JOIN ZICCLOUDSYNCINGOBJECT as blob
    on  attachment.ZMEDIA = blob.Z_PK and blob.ZATTACHMENT1 = attachment.Z_PK
WHERE
    attachment.ZTYPEUTI is not  null or attachment.ZTYPEUTI1 is not null
;



-- url public.url
SELECT
    ZIDENTIFIER as attachment_uuid, ZTYPEUTI as uti, ZNOTE as note_pk, ZTITLE as attachment_text , ZURLSTRING as url
from ZICCLOUDSYNCINGOBJECT
WHERE
    ZIDENTIFIER = '3E88F3F9-7D32-4EC1-919F-10F4034BFA16'
;

-- tag com.apple.notes.inlinetextattachment.hashtag
SELECT
    *, ZIDENTIFIER as attachment_uuid, ZTYPEUTI1 as uti, ZNOTE1 as note_pk, ZALTTEXT as attachment_text --, ZTOKENCONTENTIDENTIFIER as token
from ZICCLOUDSYNCINGOBJECT
WHERE
    ZIDENTIFIER = 'EEE0AD35-AA77-4ED4-A0B8-410864877682'
;

-- media. like public.jpeg file_path = account/media/file_uuid/generation/file_name
SELECT
    *,
    attachment.ZIDENTIFIER as attachment_uuid,
    attachment.ZTYPEUTI as uti,
    attachment.ZNOTE as note_pk,
    attachment.ZOCRSUMMARY as attachment_text,
    attachment.ZMEDIA as media_pk,
    blob.ZIDENTIFIER as file_uuid,
    COALESCE(blob.ZGENERATION, blob.ZGENERATION1) as zgeneration,
    blob.ZFILENAME as file_name
from ZICCLOUDSYNCINGOBJECT as attachment
LEFT JOIN ZICCLOUDSYNCINGOBJECT as blob
    on  attachment.ZMEDIA = blob.Z_PK and blob.ZATTACHMENT1 = attachment.Z_PK
WHERE
    attachment.ZIDENTIFIER = '330B0442-CBCB-4F52-AB1B-6F2603A04583'
    -- and attachment.ZISPASSWORDPROTECTED = 0
;


-- list all tables com.apple.notes.table
SELECT
    ZIDENTIFIER as attachment_uuid,  ZTYPEUTI as uti, ZNOTE as note_pk, ZSUMMARY as attachment_text, ZMERGEABLEDATA1 as bolb_data
from ZICCLOUDSYNCINGOBJECT
WHERE
    ZIDENTIFIER = 'C9249E24-631C-4EE5-82CC-E30E46C05902'
;

-- list all drawing 'com.apple.paper' 'com.apple.drawing.2' 'com.apple.drawing'
-- path: account/fallbackimage/attachment_uuid/generation/FallbackImage.png
-- path: account/fallbackimage/attachment_uuid.png
SELECT
    *, ZIDENTIFIER as attachment_uuid, ZTYPEUTI as uti, ZNOTE as note_pk, ZSUMMARY as attachment_text, ZFALLBACKIMAGEGENERATION as generation, ZNEEDSINITIALRELATIONSHIPSETUP
FROM ZICCLOUDSYNCINGOBJECT
WHERE
    ZTYPEUTI in ('com.apple.paper', 'com.apple.drawing.2', 'com.apple.drawing')
;

-- list gallary 'com.apple.notes.gallery'
SELECT
    *
FROM ZICCLOUDSYNCINGOBJECT
WHERE
    ZIDENTIFIER = '16E181EC-1219-45A8-B2C5-BC6AA773DC66'
;

