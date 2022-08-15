FROM nginx:1.23-alpine

ENV DJANGO_PORT=8000 
ENV DJANGO_ADMIN_URL=admin
ENV VUE_PORT=3000 

COPY prod.conf /etc/nginx/templates/default.conf.template
COPY dist /dist

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
