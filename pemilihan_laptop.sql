PGDMP         
                 {            uas_spk    14.9    14.9     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16418    uas_spk    DATABASE     g   CREATE DATABASE uas_spk WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_Indonesia.1252';
    DROP DATABASE uas_spk;
                postgres    false            �            1259    16427    laptop    TABLE       CREATE TABLE public.laptop (
    no integer NOT NULL,
    merek character varying(255) NOT NULL,
    ram character varying(255) NOT NULL,
    sistem_operasi character varying(255) NOT NULL,
    baterai character varying(255) NOT NULL,
    ukuran_layar character varying(255) NOT NULL,
    harga character varying(255) NOT NULL,
    memori_internal character varying(255) NOT NULL
);
    DROP TABLE public.laptop;
       public         heap    postgres    false            �            1259    16426    laptop_no_seq    SEQUENCE     �   CREATE SEQUENCE public.laptop_no_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.laptop_no_seq;
       public          postgres    false    210            �           0    0    laptop_no_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.laptop_no_seq OWNED BY public.laptop.no;
          public          postgres    false    209            \           2604    16430 	   laptop no    DEFAULT     f   ALTER TABLE ONLY public.laptop ALTER COLUMN no SET DEFAULT nextval('public.laptop_no_seq'::regclass);
 8   ALTER TABLE public.laptop ALTER COLUMN no DROP DEFAULT;
       public          postgres    false    210    209    210            �          0    16427    laptop 
   TABLE DATA           o   COPY public.laptop (no, merek, ram, sistem_operasi, baterai, ukuran_layar, harga, memori_internal) FROM stdin;
    public          postgres    false    210   w       �           0    0    laptop_no_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.laptop_no_seq', 10, true);
          public          postgres    false    209            ^           2606    16434    laptop laptop_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.laptop
    ADD CONSTRAINT laptop_pkey PRIMARY KEY (no);
 <   ALTER TABLE ONLY public.laptop DROP CONSTRAINT laptop_pkey;
       public            postgres    false    210            �   @  x����j� �듧8O�h/3ma����f7Yb7Y������kZba���*����cP����>X��T@��o�MkO=R�s�U�	!�->��8Em�]K)��P6�¾o#
E��N;����ONP6rU����5C@��ȔHJB��y�U}ԝ���Bb
e�\Xh�%�N����Kk�ʩo~�$N��{��t�2�U��5�/0#|
�$0�R7��v����m�F]�|:���4e�ʐ+��Y-g��;������S>]'��}��V�T�;TR��R�dS�߲2�}5xR�-.ZUWu�	� z�'I���8�����     